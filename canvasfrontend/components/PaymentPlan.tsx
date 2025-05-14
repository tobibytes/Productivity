import { usePathname } from 'next/navigation';
import React, { useEffect } from 'react'
interface PaymentPlanProps {
    stripe_payment_plan_id: string;
    stripe_public_key: string;
    id: string;
}


const PaymentPlan = ({ stripe_payment_plan_id, stripe_public_key, id }: PaymentPlanProps) => {
  const [email, setEmail] = React.useState<string | null>(null);
  const location = usePathname()

  useEffect(() => {
    const email = sessionStorage.getItem('email');
    if (email) {
      setEmail(email);
    }
  },[])
  return React.createElement(
    'stripe-pricing-table',
    {
      'pricing-table-id': stripe_payment_plan_id,
      'publishable-key': stripe_public_key,
  
      'client-reference-id': id, 
      'customer-email': email,    
    },
    null
  );
};

export default PaymentPlan