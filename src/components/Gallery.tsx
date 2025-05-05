import { useState, useEffect } from 'react';
import ImageCard from './ImageCard';
import Keywords from './Keywords';
import ImageDetail from './ImageDetail';
import '../styles/Gallery.css';
import { useMenu } from './MenuContext';


export type ImageData = {
    filename: string;
    transcription: string;
    drawings: string;
    paper: string;
    keywords: string[];
  };


function Gallery() {
    const { selectedCollection } = useMenu();

    const [images, setImages] = useState<ImageData[]>([]);
    const [keywords, setKeywords] = useState<string[]>([]);
    const [filter, setFilter] = useState<string | null>(null);
    const [selectedImage, setSelectedImage] = useState<ImageData | null>(null); // Track selected image
    const [loading, setLoading] = useState(true);

    const loadGalleryData = async () => {
        try {
          const analysis = await import(`../data/${selectedCollection.name}/analysis.json`);
          const keywordList = await import(`../data/${selectedCollection.name}/keywords.json`);
  
          setImages(analysis.default);
          setKeywords(keywordList.default);
        } catch (error) {
          console.error("Error loading gallery data:", error);
          setImages([]);
          setKeywords([]);
        } finally {
          setLoading(false);
        }
      };
  
    
    useEffect(() => {
        loadGalleryData();
      }, [selectedCollection]);
    
      if (loading) {
      }

    // Filter images based on the selected keyword
    const filteredImages = filter
        ? images.filter(image => image.keywords.includes(filter))
        : images;
 
    // Handle keyword click for filtering images
    const handleKeywordClick = (keyword: string) => {
        setFilter(current => (current === keyword ? null : keyword));
    };

    // Reset the filter to null (show all images) when the header is clicked
    const handleHeaderClick = () => {
        setFilter(null);  // Reset filter
    };

    const handleImageClick = (image: ImageData) => {
        console.log('Selected Image:', image);
        setSelectedImage(image);  // Set selected image to display in ImageDetail
    };

    const closeImageDetail = () => {
        setSelectedImage(null);  // Close the ImageDetail view
    };


    return (
        <div className="Gallery-Container">
            <div 
                className="Header"
                onClick={handleHeaderClick}
            >
                <h1>{selectedCollection.title}</h1>
            </div>
            <div className="CommonStory">
                <div className="CommonStoryText">
                    <i>{selectedCollection.common_story}</i>
                </div>
            </div>
            <div className="Keywords">
                {keywords.map((keyword) => (
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