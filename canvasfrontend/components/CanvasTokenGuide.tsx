"use client";
import Image from "next/image";

const steps = [
  {
    title: "Step 1: Go to Account",
    description: "From your Canvas dashboard, click on the **Account** button in the left sidebar.",
    image: "/gotoaccount.png",
  },
  {
    title: "Step 2: Open Settings",
    description: "Inside the account menu, click on **Settings** to access your personal settings.",
    image: "/gotosettings.png",
  },
  {
    title: "Step 3: Create a New Access Token",
    description: "Scroll down to the **Approved Integrations** section and click on **+ New Access Token**.",
    image: "/newaccesstoken.png",
  },
  {
    title: "Step 4: Generate and Copy Your Token",
    description: "Give it a name and expiry date, then click **Generate Token**. Copy the token shown — it will only be shown once!",
    image: "/generatetoken.png",
  },
];

export default function CanvasTokenGuide() {
  return (
    <div className="mx-auto px-6 py-10 bg-white rounded-lg shadow" id="howto">
      <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">How to Get Your Canvas Access Token</h1>
      <p className="text-gray-600 text-center mb-10">
        Follow these quick steps to generate your personal access token on Canvas.
      </p>

      <div className="space-y-10">
        {steps.map((step, index) => (
          <div key={index} className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-700">{step.title}</h2>
            <p className="text-gray-600">{step.description}</p>
            <div className="rounded-md overflow-hidden border border-gray-200">
              <Image
                src={step.image}
                alt={step.title}
                width={300}
                height={300}
                className=""
              />
            </div>
          </div>
        ))}
      </div>
        <p className="text-sm text-gray-500 mt-6">
            Once you have your token, <a href="#register" className="text-blue-600 hover:underline">return to the registration form</a> and paste it in the appropriate field.
        </p>
    </div>
  );
}