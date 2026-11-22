import unittest
from dataclasses import replace
from datetime import datetime,timedelta,timezone
from interval_coverage import IntervalReport,build_expected_intervals
from pricing_liability import PriceBand,PricingAgreement
from reconciliation_state_machine import Allocation,Burn,Case,Obligation,Report
from integrated_interval_reconciliation import PriorSettlement,reconcile_with_interval_coverage
UTC=timezone.utc
START=datetime(2026,11,17,12,0,tzinfo=UTC)
END=START+timedelta(minutes=10)
def make_case():
    return Case(("r0",),(Report("r0","OK","v1","o1","sync-A"),),
        (Obligation("o1",10,"v1",synchronizer_id="sync-A"),),
        (Burn("burn-1",10),),(Allocation("alloc-1","burn-1","o1",10),),
        "2026-11-17T12:10:00+00:00",reward_required=False)
def tariff():
    return PricingAgreement("agreement-A","v1","2026-11-01T00:00:00+00:00",
        None,(PriceBand(None,1),))
class PricingCorrectionIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.expected=build_expected_intervals(START,END,timedelta(minutes=10),timedelta(minutes=5))
        self.original=IntervalReport("r0",self.expected[0].interval_id,START,END,END,"OK",
            agreement_version="v1",consumed_units=10,obligation_id="o1",synchronizer_id="sync-A")
        self.prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10),)
    def test_original_report_is_priced_and_reconciles(self):
        out=reconcile_with_interval_coverage(make_case(),self.expected,(self.original,),
            pricing_agreements={"v1":tariff()})
        self.assertEqual(out["pricing_results"]["r0"]["liability_cc"],10)
        self.assertEqual(out["payment_state"],"RECONCILED")
    def test_upward_correction_reprices_and_creates_adjustment(self):
        corrected=IntervalReport("r1",self.expected[0].interval_id,START,END,END+timedelta(minutes=2),"OK",
            revision=1,supersedes_report_id="r0",agreement_version="v1",consumed_units=12,
            obligation_id="o1",synchronizer_id="sync-A")
        prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10,
            settled_amount_cc=10,
            committed_allocations=(Allocation("alloc-old","burn-1","o1",10),),
            prior_allocation_details_complete=True),)
        out=reconcile_with_interval_coverage(replace(make_case(),allocations=()),self.expected,
            (self.original,corrected),prior,
            pricing_agreements={"v1":tariff()})
        self.assertEqual(out["pricing_results"]["r1"]["liability_cc"],12)
        self.assertEqual(out["adjustments"][0]["adjustment_cc"],2)
        self.assertEqual(out["adjustments"][0]["status"],"REQUIRES_SEPARATE_SETTLEMENT")
        self.assertEqual(out["payment_state"],"SHORT_PAID")
    def test_pre_settlement_correction_uses_only_latest_report_liability(self):
        corrected=IntervalReport("r1",self.expected[0].interval_id,START,END,END+timedelta(minutes=2),"OK",
            revision=1,supersedes_report_id="r0",agreement_version="v1",consumed_units=8,
            obligation_id="o1",synchronizer_id="sync-A")
        out=reconcile_with_interval_coverage(make_case(),self.expected,(self.original,corrected),
            pricing_agreements={"v1":tariff()})
        self.assertEqual(set(out["pricing_results"]),{"r1"})
        self.assertEqual(out["pricing_results"]["r1"]["liability_cc"],8)
        self.assertEqual(out["adjustments"],[])
    def test_partial_settlement_correction_reports_remaining_balance(self):
        corrected=IntervalReport("r1",self.expected[0].interval_id,START,END,END+timedelta(minutes=2),"OK",
            revision=1,supersedes_report_id="r0",agreement_version="v1",consumed_units=12,
            obligation_id="o1",synchronizer_id="sync-A")
        prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10,
                               settled_amount_cc=5,
                               committed_allocations=(Allocation("alloc-old","burn-1","o1",5),),
                               prior_allocation_details_complete=True),)
        out=reconcile_with_interval_coverage(replace(make_case(),allocations=()),self.expected,
            (self.original,corrected),prior,
            pricing_agreements={"v1":tariff()})
        adjustment=out["adjustments"][0]
        self.assertEqual(adjustment["settlement_state"],"PARTIALLY_SETTLED")
        self.assertEqual(adjustment["adjustment_cc"],2)
        self.assertEqual(adjustment["outstanding_after_correction_cc"],7)
        self.assertEqual(adjustment["outstanding_after_new_allocations_cc"],7)
        self.assertEqual(adjustment["previous_liability_cc"]+adjustment["adjustment_cc"],
                         adjustment["revised_liability_cc"])
    def test_full_settlement_upward_correction_reports_additional_due(self):
        corrected=IntervalReport("r1",self.expected[0].interval_id,START,END,END+timedelta(minutes=2),"OK",
            revision=1,supersedes_report_id="r0",agreement_version="v1",consumed_units=12,
            obligation_id="o1",synchronizer_id="sync-A")
        prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10,
                               settled_amount_cc=10,
                               committed_allocations=(Allocation("alloc-old","burn-1","o1",10),),
                               prior_allocation_details_complete=True),)
        out=reconcile_with_interval_coverage(replace(make_case(),allocations=()),self.expected,
            (self.original,corrected),prior,
            pricing_agreements={"v1":tariff()})
        adjustment=out["adjustments"][0]
        self.assertEqual(adjustment["settlement_state"],"FULLY_SETTLED")
        self.assertEqual(adjustment["outstanding_after_correction_cc"],2)
        self.assertEqual(adjustment["credit_candidate_cc"],0)
    def test_full_settlement_downward_correction_is_credit_candidate_only(self):
        corrected=IntervalReport("r1",self.expected[0].interval_id,START,END,END+timedelta(minutes=2),"OK",
            revision=1,supersedes_report_id="r0",agreement_version="v1",consumed_units=8,
            obligation_id="o1",synchronizer_id="sync-A")
        prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10,
                               settled_amount_cc=10,
                               burn_event_ids=("burn-1",),
                               committed_allocations=(Allocation("alloc-old","burn-1","o1",10),),
                               committed_reward_record_ids=("reward-original",),
                               prior_allocation_details_complete=True),)
        correction_case=replace(make_case(),allocations=())
        out=reconcile_with_interval_coverage(correction_case,self.expected,(self.original,corrected),prior,
            pricing_agreements={"v1":tariff()})
        adjustment=out["adjustments"][0]
        self.assertEqual(adjustment["adjustment_cc"],-2)
        self.assertEqual(adjustment["credit_candidate_cc"],2)
        self.assertEqual(adjustment["status"],"REQUIRES_SEPARATE_SETTLEMENT")
        self.assertEqual(adjustment["prior_burn_event_ids"],("burn-1",))
        self.assertEqual(adjustment["prior_allocation_ids"],("alloc-old",))
        self.assertTrue(adjustment["prior_allocation_details_complete"])
        self.assertEqual(
            adjustment["reward_adjustment_state"],
            "REQUIRES_EXPLICIT_REWARD_RECONCILIATION",
        )
        self.assertEqual(out["correction_credit_policy"],"NO_AUTOMATIC_REFUND_OR_CARRY_FORWARD")
    def test_reprocessing_correction_is_idempotent_by_adjustment_id(self):
        corrected=IntervalReport("r1",self.expected[0].interval_id,START,END,END+timedelta(minutes=2),"OK",
            revision=1,supersedes_report_id="r0",agreement_version="v1",consumed_units=12,
            obligation_id="o1",synchronizer_id="sync-A")
        prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10,
            settled_amount_cc=10,
            committed_allocations=(Allocation("alloc-old","burn-1","o1",10),),
            prior_allocation_details_complete=True),)
        correction_case=replace(make_case(),allocations=())
        first=reconcile_with_interval_coverage(correction_case,self.expected,
            (self.original,corrected),prior,
            pricing_agreements={"v1":tariff()})
        adjustment_id=first["adjustments"][0]["adjustment_id"]
        replay=reconcile_with_interval_coverage(correction_case,self.expected,
            (self.original,corrected),prior,
            pricing_agreements={"v1":tariff()},processed_adjustment_ids=(adjustment_id,))
        self.assertEqual(replay["adjustments"],[])
        self.assertEqual(replay["already_processed_adjustment_ids"],(adjustment_id,))
    def test_correction_cannot_reuse_prior_burn_allocation_or_reward_credit(self):
        corrected=IntervalReport("r1",self.expected[0].interval_id,START,END,END+timedelta(minutes=2),"OK",
            revision=1,supersedes_report_id="r0",agreement_version="v1",consumed_units=12,
            obligation_id="o1",synchronizer_id="sync-A")
        prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10,
            committed_allocation_ids=("alloc-1",),committed_reward_record_ids=("reward-1",)),)
        allocation_replay=reconcile_with_interval_coverage(make_case(),self.expected,
            (self.original,corrected),prior,pricing_agreements={"v1":tariff()})
        self.assertEqual(allocation_replay["payment_state"],"BLOCKED_CORRECTION_REPLAY")
        reward_case=replace(make_case(),reward_record_ids=("reward-1",))
        prior_reward_only=(replace(prior[0],committed_allocation_ids=()),)
        reward_replay=reconcile_with_interval_coverage(reward_case,self.expected,
            (self.original,corrected),prior_reward_only,pricing_agreements={"v1":tariff()})
        self.assertEqual(reward_replay["payment_state"],"BLOCKED_CORRECTION_REPLAY")
    def test_new_allocation_cannot_reuse_consumed_burn_capacity(self):
        corrected=IntervalReport("r1",self.expected[0].interval_id,START,END,END+timedelta(minutes=2),"OK",
            revision=1,supersedes_report_id="r0",agreement_version="v1",consumed_units=12,
            obligation_id="o1",synchronizer_id="sync-A")
        prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10,
            settled_amount_cc=10,
            committed_allocations=(Allocation("alloc-old","burn-1","o1",10),),
            prior_allocation_details_complete=True),)
        correction_case=replace(make_case(),allocations=(
            Allocation("alloc-new","burn-1","o1",1),
        ))
        out=reconcile_with_interval_coverage(correction_case,self.expected,
            (self.original,corrected),prior,pricing_agreements={"v1":tariff()})
        self.assertEqual(out["payment_state"],"DISPUTED_ALLOCATION")
        self.assertIn("burn-1",out["overallocated_burns"])
    def test_incomplete_prior_allocation_history_blocks_correction_claims(self):
        corrected=IntervalReport("r1",self.expected[0].interval_id,START,END,END+timedelta(minutes=2),"OK",
            revision=1,supersedes_report_id="r0",agreement_version="v1",consumed_units=12,
            obligation_id="o1",synchronizer_id="sync-A")
        prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10,
                               settled_amount_cc=10),)
        out=reconcile_with_interval_coverage(make_case(),self.expected,(self.original,corrected),prior,
            pricing_agreements={"v1":tariff()})
        self.assertEqual(out["payment_state"],"BLOCKED_PRIOR_ALLOCATION_DETAILS_INCOMPLETE")
    def test_correction_cannot_change_prior_synchronizer_binding(self):
        corrected=IntervalReport("r1",self.expected[0].interval_id,START,END,END+timedelta(minutes=2),"OK",
            revision=1,supersedes_report_id="r0",agreement_version="v1",consumed_units=12,
            obligation_id="o1",synchronizer_id="sync-A")
        prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10,
                               synchronizer_id="sync-B"),)
        out=reconcile_with_interval_coverage(make_case(),self.expected,(self.original,corrected),prior,
            pricing_agreements={"v1":tariff()})
        self.assertEqual(out["payment_state"],"BLOCKED_CORRECTION_BINDING_CHANGED")
    def test_wrong_synchronizer_binding_blocks_pricing(self):
        bad=IntervalReport("r0",self.expected[0].interval_id,START,END,END,"OK",
            agreement_version="v1",consumed_units=10,obligation_id="o1",synchronizer_id="sync-B")
        out=reconcile_with_interval_coverage(make_case(),self.expected,(bad,),
            pricing_agreements={"v1":tariff()})
        self.assertEqual(out["payment_state"],"BLOCKED_REPORT_BINDING")
if __name__=="__main__": unittest.main()
