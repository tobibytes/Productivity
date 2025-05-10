"use client";

import { useParams } from "next/navigation";
import React, { useEffect } from "react";
import ReactMarkdown from "react-markdown";

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
  module_item_analysis: {
    title: string;
    analysis: string;
    priority: number;
  };
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
  module_item_analysis: {
    title: "AI Analysis Title",
    analysis: "This is the AI analysis content.",
    priority: 2,
  },
  module_item_markdown:
    "# Markdown Notes\n\nThis is a sample markdown note for the item.",
};

const ModuleItemPage = () => {

    const { moduleitem_id, module_id, course_id} = useParams();
    const [moduleItem, setModuleItem] = React.useState<ModuleItemPageProps>(moduleItemSample);
    const readablePriority = ["Low", "Medium", "High"][moduleItem?.module_item_analysis?.priority - 1] || "Unknown";

  useEffect(() => {
    async function fetchData() {
        const res = await fetch(`${process.env.BACKEND_URL}/modules/${module_id}/moduleitems/${moduleitem_id}`)
        const data = await res.json();
        setModuleItem(data.module_item)
    }
    fetchData()
  },[])

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">
          {moduleItem.module_item_analysis.title || moduleItem.module_item_title}
        </h1>
        <p className="text-gray-500 text-sm">
          Uploaded on {new Date(moduleItem?.module_item_created_at).toLocaleDateString()} • {Math.round(moduleItem.module_item_size / 1024)} KB
        </p>
      </header>

      <section className="mb-8 space-y-2 text-sm text-gray-700">
        <p><span className="font-medium">Filename:</span> {moduleItem?.module_item_filename}</p>
        <p><span className="font-medium">Type:</span> {moduleItem?.module_item_type} ({moduleItem.module_item_content_type})</p>
        <p><span className="font-medium">Module ID:</span> {moduleItem?.module_item_module_id}</p>
        <p><span className="font-medium">Item ID:</span> {moduleItem?.module_item_id}</p>
        <p><span className="font-medium">Priority:</span> {readablePriority}</p>

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

      <section className="mb-10">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">AI Analysis</h2>
        <div className="prose prose-sm max-w-none">
          <ReactMarkdown>{moduleItem?.module_item_analysis.analysis}</ReactMarkdown>
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Raw Markdown Notes</h2>
        <div className="prose prose-sm max-w-none">
          <ReactMarkdown>{moduleItem?.module_item_markdown}</ReactMarkdown>
        </div>
      </section>
    </div>
  );
};

export default ModuleItemPage;