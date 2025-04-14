"use client";
import { ListTodo, ChevronDown, ChevronUp } from "lucide-react";
import ReactMarkdown from "react-markdown";
import styles from "./styles.module.css";

interface TodoProps {
  todo: {
    title: string;
    from: string;
    summary: string;
    advice: string;
    due_date: string;
    priority: number;
  };
  isOpen: boolean;
  onToggle: () => void;
  index: number;
}

const getPriorityColor = (priority: number) => {
  switch (priority) {
    case 1:
      return "#00ff00";
    case 2:
      return "#0000ff";
    case 3:
      return "#ff0000";
    default:
      return "#ccc";
  }
};

export default function TodoItem({ todo, isOpen, onToggle }: TodoProps) {
  return (
    <div style={{display: 'flex'}}>
      <ListTodo color={getPriorityColor(todo.priority)} className="ml-auto" />
      <div
        className={styles.priorityContainer}
        style={{
          borderLeft: `6px solid ${getPriorityColor(todo.priority)}`,
        }}
      >
        <div
          className={styles.todoItemContainer}
          onClick={onToggle}
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
      <input type="checkbox" style={{alignSelf: 'start '}}/>
    </div>
  );
}
