"use client"
import { ListTodo, ChevronDown, ChevronUp } from "lucide-react";
import styles from "./styles.module.css";
import ReactMarkdown from "react-markdown";
import { useEffect, useState } from "react";

interface todoType {
    title: string
    from: string
    summary: string
    advice: string
    due_date: string,
    priority: number,
  }

export default function Page() {
    async function getTodo() {
        const res = await fetch('http://localhost:5000/summary/')
        const data = await res.json()
        console.log(data)
        setTodo(data)
    }
    useEffect(() => {
        async function getTodoLists() {
            await getTodo()
        }
        getTodoLists()
    },[])
    const [todo, setTodo] = useState<todoType[]>([])
  const getPriorityColor = (priority: number) => {
    switch (priority) {
      case 1:
        return "#00ff00"; // low
      case 2:
        return "#0000ff"; // medium
      case 3:
        return "#ff0000"; // high
      default:
        return "#ccc";
    }
  };

  const [expanded, setExpanded] = useState<number | null>(null);

  const toggleExpand = (index: number) => {
    setExpanded(expanded === index ? null : index);
  };

  return (
    <div className={styles.todoContainer}>
      {todo.map((todo, idx) => {
        const isOpen = expanded === idx;
        return (
          <div key={idx}>
            <ListTodo
              color={getPriorityColor(todo.priority)}
              className={styles.icon}
            />
            <div
              className={styles.priorityContainer}
              style={{
                borderLeft: `6px solid ${getPriorityColor(todo.priority)}`,
              }}
            >
              <div
                className={styles.todoItemContainer}
                onClick={() => toggleExpand(idx)}
                style={{ cursor: "pointer" }}
              >
                <div className={styles.todoHeader}>
                  <h3>{todo.title}</h3>
                  {isOpen ? <ChevronUp /> : <ChevronDown />}
                </div>
                <p className={styles.source}>From: {todo.from}</p>
                {isOpen && (
                  <>
                    <ReactMarkdown>{todo.summary}</ReactMarkdown>
                    <ReactMarkdown>{todo.advice}</ReactMarkdown>
                    <span className={styles.dueDate}>
                      🗓 Due: {new Date(todo.due_date).toDateString()}
                    </span>
                  </>
                )}
              </div>
            </div>
           <input type="checkbox" />
          </div>
        );
      })}
    </div>
  );
}
