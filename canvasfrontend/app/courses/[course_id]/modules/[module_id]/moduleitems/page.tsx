"use client";

import { useParams } from "next/navigation";
import React, { useEffect, useState } from "react";
import ModuleItemCard from "@/components/ModuleItemCard";

interface ModuleItemCardProps {
  module_item_module_id: number;
  module_item_id: number;
  module_item_title: string;
  module_item_filename: string;
  module_item_uuid: string;
  module_item_type: string;
  module_item_content_type: string;
  module_item_download_url: string;
  module_item_size: number;
  module_item_created_at: string;
  module_course_id: string;
}

export default function ModuleItemsPage() {
  const params = useParams();
  const module_id = Array.isArray(params.module_id) ? params.module_id[0] : params.module_id;
  const course_id = Array.isArray(params.course_id) ? params.course_id[0] : params.course_id;
  const [moduleItems, setModuleItems] = useState<ModuleItemCardProps[]>([]);

  useEffect(() => {
    async function fetchItems() {
      try {
        const res = await fetch(`${process.env.BACKEND_URL}/modules/${module_id}/moduleitems`);
        const data = await res.json();
        setModuleItems(data.module_items);
      } catch (error) {
        console.error("Failed to fetch module items:", error);
      }
    }

    if (module_id) fetchItems();
  }, [module_id]);

  return (
    <div className="w-full mx-auto px-6 py-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Module Items</h1>
      <div className="flex flex-wrap gap-6 justify-start">
        {moduleItems.map((item) => (
          <div
            key={item.module_item_id}
            className="w-full sm:w-1/2 md:w-1/3 lg:w-1/4"
          >
           {course_id &&  <ModuleItemCard {...item} module_course_id={course_id} /> }
          </div>
        ))}
      </div>
    </div>
  );
}