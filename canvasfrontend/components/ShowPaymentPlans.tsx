import React from 'react';
import PaymentPlan from './PaymentPlan';
const plans = [
  {
    stripe_payment_plan_id: "prctbl_1RNm71LpjISvJMPEWIHks5Wn",
    stripe_public_key: "pk_live_51MEwjTLpjISvJMPETOabPmJimxlDll0j9WY1ZL5YnSXhCzjeN5wRwLlplfndf9QlGxPc8RD9QMeRGRZdpe1dy7EX00SyyBwjYF",
  },
  {
    stripe_payment_plan_id: "prctbl_1RNmDdLpjISvJMPEikWlXfpm",
    stripe_public_key: "pk_live_51MEwjTLpjISvJMPETOabPmJimxlDll0j9WY1ZL5YnSXhCzjeN5wRwLlplfndf9QlGxPc8RD9QMeRGRZdpe1dy7EX00SyyBwjYF",
  },
  {
    stripe_payment_plan_id: "prctbl_1RNmHQLpjISvJMPEbVdjGk3J",
    stripe_public_key: "pk_live_51MEwjTLpjISvJMPETOabPmJimxlDll0j9WY1ZL5YnSXhCzjeN5wRwLlplfndf9QlGxPc8RD9QMeRGRZdpe1dy7EX00SyyBwjYF",
  }
]
function ShowPlans() {
  return (
    <div>
      <h1>Our Pricing Plans</h1>
      <div className='flex flex-wrap gap-6'>
        {plans?.map((plan) => (
<PaymentPlan stripe_payment_plan_id={plan.stripe_payment_plan_id} stripe_public_key={plan.stripe_public_key} key={plan.stripe_payment_plan_id} />

        ))}

    </div>
    </div>
  );
}

export default ShowPlans;