"use client";
import { useEffect, useState } from "react";
import TodoItem from "./todoItem";
import styles from "./styles.module.css";

interface TodoType {
  title: string;
  from: string;
  summary: string;
  advice: string;
  due_date: string;
  priority: number;
}

export default function TodoList() {
  const [todos, setTodos] = useState<TodoType[]>([]);
  const [expanded, setExpanded] = useState<number | null>(null);

  const toggleExpand = (index: number) => {
    setExpanded(expanded === index ? null : index);
  };

  async function getTodo() {
    const res = await fetch("http://localhost:5000/summary/");
    const data = await res.json();
    console.log(data);
    setTodos(data);
  }

  useEffect(() => {
    getTodo();
  }, []);

  return (
    <div className={styles.todoContainer}>
      {todos.map((todo, idx) => (
        <TodoItem
          key={idx}
          todo={todo}
          index={idx}
          isOpen={expanded === idx}
          onToggle={() => toggleExpand(idx)}
        />
      ))}
    </div>
  );
}
