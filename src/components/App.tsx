import Gallery from './Gallery'
import '../styles/App.css'
import commonStory from '../data/common_story.json';


type commonStory = {
  common_story: string;
};


function App() {
  const story: commonStory = commonStory;

  return (
    <div className="App">
      <div 
        className="Header"
        onClick={() => window.location.reload()}
      >
        <h1>etchings</h1>
      </div>
      <div className="CommonStory">
                <div className="CommonStoryText">
                    <i>{story.common_story}</i>
                </div>
            </div>
      <div className="Gallery">
        <Gallery />
      </div>
    </div>
  )
}

export default App;