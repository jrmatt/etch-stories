import React, { createContext, useContext, useState, useEffect } from "react";

// Define the structure of a collection
export type Collection = {
  name: string;
  title: string;
  common_story: string;
  aspect_ratio: string;
};

// Create a context for the selected collection
interface MenuContextType {
  selectedCollection: Collection;
  setSelectedCollection: (name: string) => void;  // Accept string (name) as parameter
}

// Default context value
const MenuContext = createContext<MenuContextType | undefined>(undefined);

// MenuProvider component to provide context to children components
export const MenuProvider = ({ children }: { children: React.ReactNode }) => {
  const [selectedCollection, setSelectedCollection] = useState<Collection | null>(null);
  const [collections, setCollections] = useState<Collection[]>([]);

  // Load all collections from the collections.json file
  useEffect(() => {
    const loadCollections = async () => {
      try {
        const response = await import("../data/collections.json"); // Load the collections.json file
        setCollections(response.default); // Save the collections data
        // Set the initial selected collection based on the first collection in the list (or use a default)
        setSelectedCollection(response.default[0]);
      } catch (error) {
        console.error("Error loading collections:", error);
      }
    };
    loadCollections();
  }, []);

  // Set the selected collection based on name
  const handleSelectCollection = (name: string) => {
    const collection = collections.find((collection) => collection.name === name);
    if (collection) {
      setSelectedCollection(collection);
    }
  };

  if (!selectedCollection) {
    return null; // or some loading state
  }

  return (
    <MenuContext.Provider value={{ selectedCollection, setSelectedCollection: handleSelectCollection }}>
      {children}
    </MenuContext.Provider>
  );
};

// Custom hook to use the MenuContext
export const useMenu = (): MenuContextType => {
  const context = useContext(MenuContext);
  if (!context) {
    throw new Error("useMenu must be used within a MenuProvider");
  }
  return context;
};