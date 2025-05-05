import { useEffect } from 'react';
import '../styles/ImageDetail.css'
import { useMenu } from './MenuContext';

interface ImageDetailProps {
    filename: string;
    transcription: string;
    drawings: string;
    paper: string;
    keywords: string[];
    onClose: () => void; // Function to close the detail view
}

function ImageDetail({ filename, drawings, transcription, onClose, paper, keywords }: ImageDetailProps ) {
    const { selectedCollection } = useMenu();


    useEffect(() => {
        document.body.classList.add('no-scroll');
        return () => {
            document.body.classList.remove('no-scroll');
        };
    }, []);

    
    return (
        <div className="ImageDetailOverlay" onClick={onClose}>
            <div className="ImageDetailContent" onClick={(e) => e.stopPropagation()}>
                <div className="image-details">
                    <p><strong>Transcript: </strong><i>{transcription}</i></p>
                    <p><strong>Drawings: </strong><i>{drawings}</i></p>
                    <p><strong>Paper: </strong><i>{paper}</i></p>
                    <div><strong>Keywords: </strong><i>{keywords.join(', ')}</i></div>
                </div>
                <img 
                    src={`/images/${selectedCollection.name}/${filename}`} alt={filename}
                    className="enlarged-image"
                    onClick={onClose} 
                />
            </div>
        </div>
    );
};

export default ImageDetail;
