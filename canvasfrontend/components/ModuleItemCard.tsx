"use client"

import { useRouter } from "next/navigation";

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
  
  const ModuleItemCard = ({
    module_item_module_id,
    module_item_id,
    module_item_title,
    module_item_filename,
    module_item_uuid,
    module_item_type,
    module_item_content_type,
    module_item_download_url,
    module_item_size,
    module_item_created_at,
    module_course_id
  }: ModuleItemCardProps) => {
    const router = useRouter()
    return (
      <div className="bg-white border border-gray-200 rounded-xl shadow p-4 hover:shadow-md transition">
        <div className="flex justify-between items-start mb-2">
          <div>
            <h3 className="text-md font-semibold text-gray-800" onClick={() => router.push(`/courses/${module_course_id}/modules/${module_item_module_id}/moduleitems/${module_item_id}`)}>{module_item_title}</h3>
            {module_item_filename && (
              <p className="text-sm text-gray-500">Filename: {module_item_filename}</p>
            )}
          </div>
          <a
            href={module_item_download_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline text-sm"
          >
            Download
          </a>
        </div>
  
        <ul className="text-sm text-gray-600 space-y-1">
          <li>
            <span className="font-medium">Module ID:</span> {module_item_module_id}
          </li>

          <li>
            <span className="font-medium">Type:</span> {module_item_type}
          </li>
          <li>
            <span className="font-medium">Created:</span>{" "}
            {new Date(module_item_created_at).toLocaleString()}
          </li>
        </ul>
      </div>
    );
  };
  
  export default ModuleItemCard;