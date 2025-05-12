import React from 'react'
interface PaymentPlanProps {
    stripe_payment_plan_id: string;
    stripe_public_key: string;
}


const PaymentPlan = ( {stripe_payment_plan_id, stripe_public_key } : PaymentPlanProps) => {
  return (
    <stripe-pricing-table pricing-table-id={stripe_payment_plan_id}
publishable-key={stripe_public_key}>
</stripe-pricing-table>
  )
}

export default PaymentPlan