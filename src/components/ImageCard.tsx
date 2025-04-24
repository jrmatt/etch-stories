import '../styles/ImageCard.css';
import { useState } from 'react';
import { ImageData } from './Gallery'
 
interface ImageCardProps {
    filename: string;
    transcription: string;
    drawings: string;
    paper: string;
    keywords: string[];
    onClick: (image: ImageData) => void;
}

function ImageCard({ filename, drawings, transcription, paper, keywords, onClick }: ImageCardProps ) {
    const [hovered, setHovered] = useState(false);

    return (
        <div 
            className="image-card"
            onMouseEnter={() => setHovered(true)}
            onMouseLeave={() => setHovered(false)}
            onClick={() => onClick({filename, transcription, drawings, paper, keywords })}
        >
            <img src={`/images/${filename}`} alt={filename} />
            {hovered && <div className="overlay">
                <div className="overlay-text">
                    <p className="transcription">"{transcription}"</p>
                    <p>{drawings}</p>
                </div>
            </div>}
        </div>
    )
}

export default ImageCard;