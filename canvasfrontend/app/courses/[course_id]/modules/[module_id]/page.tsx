"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import ModuleItemCard from "@/components/ModuleItemCard";
import ModuleCard from "@/components/ModuleCard";

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

interface ModuleData {
  module_id: string;
  module_course_id: string;
  module_name: string;
  module_completed_at: string | null;
  module_state: string;
  module_prerequisite_ids: number[];
}

export default function ModulePage() {
  const { course_id, module_id } = useParams();
  const [module, setModule] = useState<ModuleData | null>(null);
  const [moduleItems, setModuleItems] = useState<ModuleItemCardProps[]>([]);

  useEffect(() => {
    async function fetchModule() {
      try {
        const res = await fetch(`${process.env.BACKEND_URL}/courses/${course_id}/modules/${module_id}`);
        const data = await res.json();
        setModule(data.module);
      } catch (error) {
        console.error("Error fetching module data:", error);
      }
    }

    async function fetchModuleItems() {
      try {
        const res = await fetch(`${process.env.BACKEND_URL}/modules/${module_id}/moduleitems`);
        const data = await res.json();
        setModuleItems(data.module_items);
      } catch (error) {
        console.error("Error fetching module items:", error);
      }
    }

    if (course_id && module_id) {
      fetchModule();
      fetchModuleItems();
    }
  }, [course_id, module_id]);

  if (!module) {
    return <div className="text-center py-10 text-gray-500">Loading module...</div>;
  }

  return (
    <div className="w-full overflow-x-hidden">
      <div className="max-w-7xl mx-auto px-4 py-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-4">{module.module_name}</h1>

        <div className="mb-8">
          <ModuleCard {...module} />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {moduleItems.map((item) => (
            <div key={item.module_item_id}>
              <ModuleItemCard {...item} module_course_id={module.module_course_id} />
            </div>
          ))}
        </div>
        {moduleItems.length === 0 && (
          <div className="w-full text-center py-10 text-gray-500">
            No module items available for this module. Please check back later.
          </div>
        )}
      </div>
    </div>
  );
}
