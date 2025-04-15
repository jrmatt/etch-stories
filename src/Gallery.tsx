import { useState } from 'react';
import ImageCard from './ImageCard';
import Keywords from './Keywords';
import ImageDetail from './ImageDetail';
import './Gallery.css';
import analysis from './data/analysis.json';
import keywordList from './data/keywords.json';

export type ImageData = {
    filename: string;
    transcription: string;
    drawings: string;
    paper: string;
    keywords: string[];
  };


function Gallery() {
    const images: ImageData[] = analysis;
    const displayKeywords: string[] = keywordList;
    const [filter, setFilter] = useState<string | null>(null);
    const [selectedImage, setSelectedImage] = useState<ImageData | null>(null); // Track selected image


    const filteredImages = filter
        ? images.filter(image => image.keywords.includes(filter))
        : images;
 
    const handleKeywordClick = (keyword: string) => {
        setFilter(current => (current === keyword ? null : keyword));
    };

    const handleImageClick = (image: ImageData) => {
        console.log('Selected Image:', image);
        setSelectedImage(image);  // Set selected image to display in ImageDetail
    };

    const closeImageDetail = () => {
        setSelectedImage(null);  // Close the ImageDetail view
    };

    return (
        <div>
            <div className="Keywords">
                {displayKeywords.map((keyword) => (
                        <Keywords 
                            key={keyword} 
                            keyword={keyword} 
                            isActive={filter === keyword} 
                            onClick={handleKeywordClick}                        
                        />
                ))}

            </div>
            <div className="Images">
            {filteredImages.map(image => {
                return (
                    <div key={image.filename}>
                        <ImageCard 
                            filename={image.filename}
                            transcription={image.transcription}
                            drawings={image.drawings}
                            paper={image.paper}
                            keywords={image.keywords}
                            onClick= {handleImageClick}
                        />
                    </div>
                );
            })}
            </div>
            {selectedImage && (
                <ImageDetail 
                    {...selectedImage}  // Pass all image props to ImageDetail
                    onClose={closeImageDetail}  // Pass the close handler to ImageDetail
                />
            )}
        </div>
    )
};

export default Gallery;