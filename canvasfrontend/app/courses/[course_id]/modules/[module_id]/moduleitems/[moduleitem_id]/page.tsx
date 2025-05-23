"use client";

import dynamic from "next/dynamic";
import { useParams, useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";
import Markdown from "react-markdown";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
const Slides = dynamic(() => import("@/components/Slides"), { ssr: false });

interface ModuleItemPageProps {
  module_item_module_id: string;
  module_item_id: string;
  module_item_title: string;
  module_item_filename: string;
  module_item_uuid: string;
  module_item_type: string;
  module_item_content_type: string;
  module_item_download_url: string;
  module_item_size: number;
  module_item_created_at: string;
  // module_item_analysis: {
  //   analysis: string;
  // };
  module_item_markdown: string;
}

const moduleItemSample : ModuleItemPageProps= {
  module_item_module_id: "278723",
  module_item_id: "6126236",
  module_item_title: "test",
  module_item_filename: "test",
  module_item_uuid: "test",
  module_item_type: "pdf",
  module_item_content_type: "test",
  module_item_download_url:
    "test",
  module_item_size: 128540,
  module_item_created_at: "2025-02-07T12:20:43Z",
  // module_item_analysis: {
  //   title: "AI Analysis Title",
  //   analysis: "This is the AI analysis content.",
  //   priority: 2,
  // },
  module_item_markdown:
    "# Markdown Notes\n\nThis is a sample markdown note for the item.",
};

const ModuleItemPage = () => {

    const { moduleitem_id, module_id, course_id} = useParams();
    const [moduleItem, setModuleItem] = useState<ModuleItemPageProps>(moduleItemSample);
    const [AiNotes, setAiNotes] = useState("")
    const [slideNotes, setSlideNotes] = useState("")
    // const readablePriority = ["Low", "Medium", "High"][moduleItem?.module_item_analysis?.priority - 1] || "Unknown";

    const [is_subscribed, setIsSubscribed] = useState(false);


    async function fetchSubscription() {
      try {
        const res = await fetch(`${process.env.BACKEND_URL}/users/${sessionStorage.getItem("email")}`);
        const data = await res.json();
        setIsSubscribed(data.user.pricing_id);
      }
      catch (error) {
        console.error("Error fetching subscription data:", error);
      }
    }

    async function fetchNote() {
      try {
        const email = sessionStorage.getItem("email")
        const res = await fetch(`${process.env.BACKEND_URL}/moduleitems/${moduleitem_id}/note?email=${email}`)
        const data = await res.json()
        if (data.note) {
          console.log("Fetched note data:", data.note)
          setAiNotes(data.note.analysis)
          setSlideNotes(data.note.slide)
        }
        else {
          setAiNotes("Could not analyze")
          setSlideNotes("Could not analyze")
        }
      }
      catch (error) {
        console.log("Error getting user's notes")
      }
    }
    
    useEffect(() => {

      fetchNote()

    },[])
    
    useEffect(() => {
      async function fetchData() {
        const res = await fetch(`${process.env.BACKEND_URL}/modules/${module_id}/moduleitems/${moduleitem_id}`)
        const data = await res.json();
        setModuleItem(data.module_item)
      }
      fetchSubscription();
      fetchData()
  },[is_subscribed])

  const router = useRouter();
  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <header className="mb-8">
        {/* <h1 className="text-3xl font-bold text-gray-800">
          {moduleItem.module_item_analysis.title || moduleItem.module_item_title}
        </h1> */}
        <p className="text-gray-500 text-sm">
          Uploaded on {new Date(moduleItem?.module_item_created_at).toLocaleDateString()} • {Math.round(moduleItem.module_item_size / 1024)} KB
        </p>
      </header>

      <section className="mb-8 space-y-2 text-sm text-gray-700">
        <p><span className="font-medium">Filename:</span> {moduleItem?.module_item_filename}</p>
        <p><span className="font-medium">Type:</span> {moduleItem?.module_item_type} ({moduleItem.module_item_content_type})</p>
        <p><span className="font-medium">Module ID:</span> {moduleItem?.module_item_module_id}</p>
        <p><span className="font-medium">Item ID:</span> {moduleItem?.module_item_id}</p>
        {/* <p><span className="font-medium">Priority:</span> {readablePriority}</p> */}

        <a
          href={moduleItem?.module_item_download_url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        >
          Download File
        </a>
      </section>

      <hr className="my-8" />
      {
        is_subscribed && <button className="bg-blue-500 text-white px-4 py-2 rounded mb-4 cursor-pointer" onClick={() => router.push(`/courses/${course_id}/modules/${module_id}/moduleitems/${moduleitem_id}/flashcards`)}>Go to Flashcards</button>
      }
      {!is_subscribed && <button className="bg-blue-500 text-white px-4 py-2 rounded mb-4 cursor-pointer" onClick={() => router.push(`/pricing`)}>Subscribe to view flashcards</button>}

      <section className="mb-10">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">AI Analysis</h2>
        <div className="prose prose-sm max-w-none">
          {is_subscribed && <Markdown remarkPlugins={[remarkGfm]}>{AiNotes}</Markdown>}
          {!is_subscribed && (
            <p className="text-gray-500">
              You need to subscribe to view the AI analysis. Please check our <a href="/pricing" className="text-blue-600">pricing plans</a>.
            </p>
          )}
        </div>
      </section>

      {/* <section>
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Raw Markdown Notes</h2>
        <div className="prose prose-sm max-w-none">
          <Markdown remarkPlugins={[remarkGfm]}>{moduleItem?.module_item_markdown}</Markdown>
        </div>
      </section> */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">AI Slide</h2>
        <div className="prose prose-sm max-w-none">
          {is_subscribed && <Slides markdownText={slideNotes} /> }
          {!is_subscribed && (
            <p className="text-gray-500">
              You need to subscribe to view the AI slides. Please check our <a href="/pricing" className="text-blue-600">pricing plans</a>.
            </p>
          )}
        </div>
      </section>
    </div>
  );
};

export default ModuleItemPage;