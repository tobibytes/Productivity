'use client'
import { AudioLines, Camera, ChevronLeft, ChevronRight, CirclePlus, FolderClosed, Image, Mic, SquarePen } from "lucide-react";


export function ChatContainer() {
    return (
        <div className="chat-container">
        <header className="">
            <ChevronLeft />
            <div className="header-img"><img /></div>
            <p>Tobi</p>
            <ChevronRight size={20}/>
            <SquarePen className="ml-auto"/>
        </header>
        <hr color="red"/>

        <div className="input-container">
            <textarea placeholder="Message Tobi" cols={33} rows={2} />
            <div className="file-modal">
                    <div>
                        <label className="file-upload">

                        <input className="file-upload" type="file" /><p>Attach Photos</p> <Image size={32} color="#21426e" strokeWidth={0.5} />
                        </label>
                    </div>
                    <hr />
                    <div>
                        <label className="file-upload">

                        <input className="file-upload" type="file" /><p>Take Photo</p>  <Camera size={32} color="#21426e" strokeWidth={0.5} />
                        </label>
                    </div>
                    <hr />
                    <div>
                        <label className="file-upload">

                        <input className="file-upload" type="file" /><p>Attach Files</p>  <FolderClosed size={32} color="#21426e" strokeWidth={0.5} />
                        </label>
                    </div>
            </div>
            <footer className="">
            <CirclePlus className="file-input default" size={32} strokeWidth={0.5} onClick={()=>{}}/>
            <Mic size={32} color="#c81414" strokeWidth={0.5} className="ml-auto icon"/>
            <AudioLines size={32} color="#c81414" strokeWidth={0.5} />
            </footer>
        </div>
        </div>
    )
}