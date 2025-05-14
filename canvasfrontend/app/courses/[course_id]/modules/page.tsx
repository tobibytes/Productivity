"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import ModuleCard from "@/components/ModuleCard";

interface ModuleCardProps {
  module_course_id: string;
  module_id: string;
  module_name: string;
  module_completed_at: string | null;
  module_state: string;
  module_prerequisite_ids: number[];
}

const ModulesPage = () => {
  const { course_id } = useParams();
  const [modules, setModules] = useState<ModuleCardProps[]>([]);
  const [email, setEmail] = useState<string | null>(null);

  useEffect(() => {
    const emailFromStorage = sessionStorage.getItem("email");
    if (emailFromStorage) {
      setEmail(emailFromStorage);
    } else {
      console.error("Email not found in session storage");
    }
  }, []);

  useEffect(() => {
    async function fetchModules() {
      try {
        const res = await fetch(`${process.env.BACKEND_URL}/courses/${course_id}/modules?email=${email}`);
        const data = await res.json();
        setModules(data.modules);
      } catch (error) {
        console.error("Error fetching modules:", error);
      }
    }

    if (course_id && email) fetchModules();
  }, [course_id, email]);

  return (
    <div className="p-6 flex flex-wrap gap-6 justify-start">
      {modules.map((mod) => (
        <div key={mod.module_id} className="w-full sm:w-1/2 md:w-1/3 xl:w-1/4">
          <ModuleCard {...mod} />
        </div>
      ))}
      {modules.length === 0 && (
        <div className="w-full text-center py-10 text-gray-500">
          No modules available for this course. Please check back later.  
    </div>
      )}
      </div>
  );
};

export default ModulesPage;
