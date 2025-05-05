import { MenuProvider } from "./MenuContext";
import { useState } from 'react';
import Menu from "./CollectionMenu";
import Gallery from "./Gallery";
import Home from "./Home";


const App = () => {

  const [showMainApp, setShowMainApp] = useState(false);

  return (
      <div className="App">
        {showMainApp ? (
          <MenuProvider>
            <Menu />
            <Gallery />
          </MenuProvider>
        ) : (
          <Home onEnter={() => setShowMainApp(true)} />
        )}
      </div>
  );
};

export default App;