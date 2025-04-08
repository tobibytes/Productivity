'use client'

import { AudioLines, Camera, ChevronLeft, ChevronRight, CircleArrowUp, CirclePlus, FolderClosed, Image, Mic, SendHorizontal, SquarePen, X } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

interface MessageType {
    type: 'audio' | 'text' | 'image' | 'document' | 'link' | 'file'
    content: ImageType | AudioType | VideoType | LinkType | DocumentType | string
    timestamp: string
    id: number
}

interface InputType {
    type: 'text' | 'file';
    content: FileInput[] | string
    id: number;
    timestamp: string;
}

interface ImageType {
    url: string;
}

interface AudioType {
    url: string
}

interface VideoType {
    url: string
}

interface DocumentType {
    url: string
}

interface FileInput {
    name: string;
    content: string | ArrayBuffer | null;
}

interface LinkType {
    name: string;
    url: string;
}

const messageData: MessageType[] = [
    { id: 1, type: 'text', content: 'Hello, world!', timestamp: '2025-04-02:12:00:00' },
    { id: 2, type: 'image', content: { url: 'https://loremflickr.com/320/240' }, timestamp: '2025-04-02:12:05:30' },
    { id: 3, type: 'link', content: { name: 'Google', url: 'https://google.com' }, timestamp: '2025-04-02:12:10:15' },
    { id: 4, type: 'text', content: 'How’s it going?', timestamp: '2025-04-02:12:12:45' },
    { id: 5, type: 'image', content: { url: 'https://loremflickr.com/320/240' }, timestamp: '2025-04-02:12:15:00' },
    { id: 6, type: 'link', content: { name: 'GitHub', url: 'https://github.com' }, timestamp: '2025-04-02:12:18:25' },
    { id: 7, type: 'text', content: 'Check this out!', timestamp: '2025-04-02:12:22:10' },
    { id: 8, type: 'image', content: { url: 'https://loremflickr.com/320/240' }, timestamp: '2025-04-02:12:25:30' },
    { id: 9, type: 'link', content: { name: 'Reddit', url: 'https://reddit.com' }, timestamp: '2025-04-02:12:30:45' },
    { id: 10, type: 'text', content: 'Today is a great day.', timestamp: '2025-04-02:12:35:50' },
    { id: 11, type: 'image', content: { url: 'https://loremflickr.com/320/240' }, timestamp: '2025-04-02:12:40:20' },
    { id: 12, type: 'link', content: { name: 'YouTube', url: 'https://youtube.com' }, timestamp: '2025-04-02:12:45:10' },
    { id: 13, type: 'text', content: 'Here’s a random thought...', timestamp: '2025-04-02:12:50:30' },
    { id: 14, type: 'image', content: { url: 'https://loremflickr.com/320/240' }, timestamp: '2025-04-02:12:55:15' },
    { id: 15, type: 'link', content: { name: 'Stack Overflow', url: 'https://stackoverflow.com' }, timestamp: '2025-04-02:13:00:00' },
    { id: 16, type: 'text', content: 'Anyone up for a coffee?', timestamp: '2025-04-02:13:05:40' },
    { id: 17, type: 'image', content: { url: 'https://loremflickr.com/320/240' }, timestamp: '2025-04-02:13:10:55' },
    { id: 18, type: 'link', content: { name: 'Twitter', url: 'https://twitter.com' }, timestamp: '2025-04-02:13:15:20' },
    { id: 19, type: 'text', content: 'This is a test message.', timestamp: '2025-04-02:13:20:30' },
    { id: 20, type: 'image', content: { url: 'https://loremflickr.com/320/240' }, timestamp: '2025-04-02:13:25:45' },
];


export function ChatContainer() {
    const [messages, setMessages] = useState<MessageType[] | InputType[]>(messageData);
    const [input, setInput] = useState<InputType>({ type: 'text', content: '', id: 1, timestamp: Date.now().toString() });
    const [filePreview, setFilePreview] = useState<FileInput[]>([]);
    const [textInput, setTextInput] = useState("")
    const router = useRouter();

    useEffect(() => {
        router.push("#last-message");
    }, [router]);

    function handleSend() {
        if (input.type === "text") {
            setMessages((prev => [...prev, input]))
            console.log(input)
        }
    }

    function handleRemoveFile(content: string | ArrayBuffer | null) {
        setFilePreview((prev) => prev.filter((file) => file.content !== content));
    }

    const [position, setPosition] = useState({ x: 0, y: 0 });
    const [dragging, setDragging] = useState(false);
    const [startPos, setStartPos] = useState({ x: 0, y: 0 });

    useEffect(() => {
        setInput({content: filePreview, timestamp: '2025-04-03', id: 1, type: 'file'})
    }, [filePreview])

    useEffect(() => {
        const onMouseMove = (e: MouseEvent) => {
            if (dragging) {
                setPosition({
                    x: e.clientX - startPos.x,
                    y: e.clientY - startPos.y,
                });
            }
        };

        const onMouseUp = () => {
            setDragging(false);
            window.removeEventListener("mousemove", onMouseMove);
            window.removeEventListener("mouseup", onMouseUp);
        };

        if (dragging) {
            window.addEventListener("mousemove", onMouseMove);
            window.addEventListener("mouseup", onMouseUp);
        } else {
            window.removeEventListener("mousemove", onMouseMove);
            window.removeEventListener("mouseup", onMouseUp);
        }

        return () => {
            window.removeEventListener("mousemove", onMouseMove);
            window.removeEventListener("mouseup", onMouseUp);
        };
    }, [dragging, startPos]);

    const onMouseDown = (e: React.MouseEvent) => {
        setDragging(true);
        setStartPos({
            x: e.clientX - position.x,
            y: e.clientY - position.y,
        });
    };
    return (
        <div className="chat-container resizable" draggable={true} onMouseDown={onMouseDown} style={{
            position: "absolute",
            top: `${position.y}px`,
            left: `${position.x}px`,
            cursor: dragging ? "grabbing" : "grab",
        }}>
            <header>
                <ChevronLeft />
                <div className="header-img"><img /></div>
                <p>Tobi</p>
                <ChevronRight size={20} />
                <SquarePen className="ml-auto" />
            </header>
            <hr color="red" />
            <div className="messages-container">
                {
                    messages.map((msg, index) => (
                        <div key={index} className={`message ${msg.type}`} id={`${index}`}>
                        { msg.type === 'text' && <p>{msg.content}</p> }
                        { msg.type === 'image' && <img src={msg.content.url} alt="" /> }
                        {
                            msg.type === 'link' && <Link className="message link" href={msg.content.url} target="_blank">
                                <div className="link-content">
                                    <p className="link-name">{msg.content.name}</p>
                                    <p className="link-url">{msg.content.url}</p>
                                </div>
                            </Link>
                        }
                        </div>

                    ))
                }
                <div id="last-message"></div>
            </div>
            {filePreview.length > 0 ? <div className="file-preview-container">
                {filePreview.length > 0 && filePreview.map((preview, index) => (
                    <div className="file-preview" key={index}>
                        {typeof preview.content === "string" && <img src={preview.content} alt="" />}
                        <X className="cancel-button" color="red" onClick={() => handleRemoveFile(preview.content)} />
                    </div>
                ))}
            </div>
                : <></>}
            <div className="input-container">
                <textarea placeholder="Message Tobi" cols={33} rows={2} onChange={
                    (e) => {
                        // setTextInput(e.target.value);
                        setInput({type: 'text', content: e.target.value, id: 1, timestamp: '2025-04-02:14:36:50'})
                    }
                } />
                <footer>
                    <input type="checkbox" id="file-modal-checkbox" />
                    <CirclePlus className="file-input" size={32} strokeWidth={0.5} onClick={() => { }} />
                    <div className="file-modal">
                        <div>
                            <label>
                                <input className="file-upload" type="file" />
                                <p>Attach Photos</p>
                                <Image size={32} color="#21426e" strokeWidth={0.5} />
                            </label>
                        </div>
                        <hr />
                        <div>
                            <label>
                                <input className="file-upload" type="file" />
                                <p>Take Photo</p>
                                <Camera size={32} color="#21426e" strokeWidth={0.5} />
                            </label>
                        </div>
                        <hr />
                        <div>
                            <label>
                                <input
                                    id="file-input"
                                    className="file-upload"
                                    type="file"
                                    onChange={(e) => {
                                        if (e.target.files) {
                                            for (let i = 0; i < e.target.files.length; i++) {
                                                console.log(i)
                                                const inputFile = e.target.files[i];
                                                const reader = new FileReader();

                                                reader.onload = (g) => {
                                                    if (g.target && g.target !== null && typeof g.target?.result === "string") {
                                                        setFilePreview((prev) => [
                                                            ...prev,
                                                            { name: `picture ${i}`, content: g.target.result }
                                                        ]);     
                                                    }
                                                };
                                                reader.readAsDataURL(inputFile);
                                            }
                                        }
                                    }}
                                />
                                <p>Attach Files</p>
                                <FolderClosed size={32} color="#21426e" strokeWidth={0.5} />
                            </label>
                        </div>
                    </div>
                    <Mic size={32} color="#c81414" strokeWidth={0.5} className="ml-auto icon" />
                    <AudioLines size={32} color="#c81414" strokeWidth={0.5} onClick={() => console.log(2, filePreview)} />
                    <SendHorizontal className="" size={32} onClick={handleSend}/>
                </footer>
            </div>
        </div>
    );
}
