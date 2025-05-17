'use client';
import React, { useEffect, useState } from 'react';
import PaymentPlan from './PaymentPlan';


interface PlanType {
  pricing_table_id: string;
  stripe_public_key: string;
  id: string;
  is_active: boolean
}

function ShowPlans() {
  const [plans, setPlans] = useState<PlanType[]>([]);
  const stripe_public_key = process.env.STRIPE_PUBLIC_KEY || "";
  const [userPlan, setUserPlan] = useState<PlanType | null>(null);
  useEffect(() => {
    const email = sessionStorage.getItem('email');

    async function fetchPlans() {
      const response = await fetch(`${process.env.PAYMENT_URL}/pricings?email=${email}`);
      const data = await response.json();
      const userCurrentPlan = data.pricings.filter((plan: PlanType) => plan.is_active === true);
      const otherPlans = data.pricings.filter((plan: PlanType) => plan.is_active === false);
      setUserPlan(userCurrentPlan[0]);
      setPlans(otherPlans);
    }
    // if (email) {
      fetchPlans()
    // }
  },[])

  return (
    <div>
      <h1>Our Pricing Plans</h1>
      <div className='flex flex-wrap gap-6'>
        <div className='w-full'>
        {userPlan && (
          <>
            <h2 className='text-lg font-bold'>Your Current Plan : <p className='text-amber-500'>Subscribed</p></h2>
            <PaymentPlan stripe_payment_plan_id={userPlan.pricing_table_id} stripe_public_key={stripe_public_key} id={userPlan.id} key={userPlan.pricing_table_id} />
          </>
        )}

        </div>
        <h2 className='text-lg font-bold'>Other Plans</h2>

        {plans?.map((plan) => (
        <PaymentPlan stripe_payment_plan_id={plan.pricing_table_id} stripe_public_key={stripe_public_key} id={plan.id} key={plan.pricing_table_id} />
        ))}
    </div>

    </div>
  );
}

export default ShowPlans;