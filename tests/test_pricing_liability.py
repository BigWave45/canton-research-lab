import unittest
from dataclasses import dataclass
from pricing_liability import PriceBand,PricingAgreement,calculate_liability

@dataclass(frozen=True)
class SyntheticReport:
    report_id:str
    status:str
    agreement_version:str
    interval_start:str
    interval_end:str
    consumed_units:int

START="2026-11-17T12:00:00+00:00"
END="2026-11-17T12:10:00+00:00"

def report(units=100,version="v1",status="OK"):
    return SyntheticReport("r1",status,version,START,END,units)

def agreement(**kw):
    base=dict(agreement_id="a1",version_id="v1",effective_from="2026-11-01T00:00:00+00:00",
              effective_until=None,bands=(PriceBand(None,2),))
    base.update(kw)
    return PricingAgreement(**base)

class PricingLiabilityTests(unittest.TestCase):
    def test_fixed_rate(self):
        self.assertEqual(calculate_liability(report(),agreement())["liability_cc"],200)
    def test_progressive_bands(self):
        a=agreement(bands=(PriceBand(50,2),PriceBand(None,1)))
        self.assertEqual(calculate_liability(report(100),a)["liability_cc"],150)
    def test_discount_and_fixed_fee(self):
        a=agreement(discount_basis_points=1000,fixed_fee_cc=5)
        self.assertEqual(calculate_liability(report(),a)["liability_cc"],185)
    def test_ceiling_rounding(self):
        a=agreement(bands=(PriceBand(None,1),),discount_basis_points=3333)
        self.assertEqual(calculate_liability(report(2),a)["liability_cc"],2)
    def test_floor_rounding(self):
        a=agreement(bands=(PriceBand(None,1),),discount_basis_points=3333,rounding="FLOOR")
        self.assertEqual(calculate_liability(report(2),a)["liability_cc"],1)
    def test_wrong_agreement_version_rejected(self):
        with self.assertRaises(ValueError): calculate_liability(report(version="v2"),agreement())
    def test_non_ok_report_rejected(self):
        with self.assertRaises(ValueError): calculate_liability(report(status="UNDETERMINED"),agreement())
    def test_agreement_must_cover_interval(self):
        a=agreement(effective_until="2026-11-17T12:05:00+00:00")
        with self.assertRaises(ValueError): calculate_liability(report(),a)
    def test_negative_units_rejected(self):
        with self.assertRaises(ValueError): calculate_liability(report(-1),agreement())
    def test_insufficient_bands_rejected(self):
        a=agreement(bands=(PriceBand(50,2),))
        with self.assertRaises(ValueError): calculate_liability(report(100),a)

if __name__=="__main__": unittest.main()
