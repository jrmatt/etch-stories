import { MenuProvider } from "./MenuContext";
import Menu from "./CollectionMenu";
import Gallery from "./Gallery";

const App = () => {
  return (
    <MenuProvider>
      <div className="App">
        <Menu />
        <Gallery />
      </div>
    </MenuProvider>
  );
};

export default App;