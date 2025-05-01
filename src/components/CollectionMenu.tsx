import { useState } from "react";
import { useMenu } from "./MenuContext";
import collections from "../data/collections.json";
import "../styles/Menu.css"

type Collection = {
  name: string;
  title: string;
};

export default function Menu() {
  const [open, setOpen] = useState(false);
  const { selectedCollection, setSelectedCollection } = useMenu();

  const handleSelect = (collection: Collection) => {
    setSelectedCollection(collection.name);  // Pass only the collection name
    setOpen(false);
  };

  return (
    <div className="menu-button-div">
      <button
        onClick={() => setOpen(!open)}
        className={`menu-button ${open ? "open" : ""}`}
      >
        <h4>view collections</h4>
      </button>

      {open && (
        <div 
          className="collections-options"
          >
          {collections.map((collection: Collection) => (
            <button
              key={collection.name}
              onClick={() => handleSelect(collection)}
              className={`collection-item ${
                selectedCollection?.name === collection.name
                  ? "selected"
                  : ""
              }`}
            >
              <h4>{collection.title}</h4>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}