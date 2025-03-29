'use client'
import { Blob, File } from "buffer";
import { AudioLines, Camera, ChevronLeft, ChevronRight, CircleArrowUp, CirclePlus, FolderClosed, Image, Mic, SquarePen } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const data = [
    { type: 'text', content: 'hello nice to meet you ', sender: 1 },
    { type: 'file', content: 'https://linktoafile.com/file', sender: 1 },
    { type: 'text', content: 'hello nice to meet you ', sender: 2 },
    { type: 'text', content: 'hello nice to meet you ', sender: 1 },
    { type: 'text', content: 'hello nice to meet you ', sender: 2 },
]
const types = ["date", "text", "file", "image", "video", "audio"]

interface inputType {
    type: 'text' | 'file' | 'audio' | 'image' | 'link';
    content: FileInput | string | LinkInput | ImageType | VideoType | AudioType;
    sender: number;
    date: number;
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
interface FileInput {
    name: string;
    blob: Blob
}
interface LinkInput {
    name: string;
    url: string;
}
export function ChatContainer() {
    const [messages, setMessages] = useState<inputType[]>([])
    const [input, setInput] = useState<inputType>({ type: 'text', content: '', sender: 1, date: Date.now() })
    const [filePreview, setFilePreview] = useState<FileInput>()
    const router = useRouter()
    useEffect(() => {
        router.push("#last-message")
    }, [])
    function handleSend() {
        setMessages((prev) => [...prev, input])
    }
    return (
        <div className="chat-container">
            <header className="">
                <ChevronLeft />
                <div className="header-img"><img /></div>
                <p>Tobi</p>
                <ChevronRight size={20} />
                <SquarePen className="ml-auto" />
            </header>
            <hr color="red" />
            <div className="messages-container">
                <div id="top-message" className="message text"><p>this is a message2</p></div>
                <div className="message text"><p>this is a message3</p></div>
                <div className="message text"><p>this is a message4</p></div>
                <div className="message text"><p>this is a message4</p></div>
                <div className="message text"><p>this is a message4</p></div>
                <div className="message text"><p>this is a message4</p></div>
                <div className="message text"><p>this is a message4</p></div>
                <div className="message text"><p>this is a message4</p></div>
                <div className="message text"><p>this is a message4</p></div>
                <div className="message text"><p>this is a message4</p></div>
                <div className="message text"><p>this is a message4</p></div>
                <div className="message text"><p>this is a message4</p></div>
                <div className="message text"><p>this is a message4</p></div>
                <div className="message text"><p>this is a message4</p></div>
                <div className="message text"><p>this is a message4</p></div>
                <div className="message text"><p>this is a message4</p></div>
                <div className="message text"><p>this is a message4</p></div>
                <div className="message text"><p>this is a message4</p></div>
                <Link className="message link" href={"https://www.google.com"}><div className="link-content"><p className="link-name">google</p><p className="link-url">www.google.com</p></div></Link>
                <div id="last-message" className="message text"><p>this is a message4</p></div>
            </div>
            {filePreview ? (
                <div>
                    
                </div>
            ) : <></>}
            <div className="input-container">
                <textarea placeholder="Message Tobi" cols={33} rows={2} />
                <footer className="">
                    <input type="checkbox" id="file-modal-checkbox"/>
                    <CirclePlus className="file-input" size={32} strokeWidth={0.5} onClick={() => { }} />
                    <div className="file-modal">
                        <div>
                            <label >

                                <input className="file-upload" type="file" /><p>Attach Photos</p> <Image size={32} color="#21426e" strokeWidth={0.5} />
                            </label>
                        </div>
                        <hr />
                        <div>
                            <label >

                                <input className="file-upload" type="file" /><p>Take Photo</p>  <Camera size={32} color="#21426e" strokeWidth={0.5} />
                            </label>
                        </div>
                        <hr />
                        <div>
                            <label>

                                <input id="file-input" className="file-upload" type="file" /><p>Attach Files</p>  <FolderClosed size={32} color="#21426e" strokeWidth={0.5} />
                            </label>
                        </div>
                    </div>
                    <Mic size={32} color="#c81414" strokeWidth={0.5} className="ml-auto icon" />
                    <AudioLines size={32} color="#c81414" strokeWidth={0.5} />
                    <CircleArrowUp size={32} color="#21426e" strokeWidth={0.5} className="hidden" />
                </footer>
            </div>
        </div>
    )
}