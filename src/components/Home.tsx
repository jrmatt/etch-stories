import "../styles/Home.css"

interface HomeProps {
    onEnter: () => void;
  }
  
  const Home: React.FC<HomeProps> = ({ onEnter }) => {
    return (
      <div className="home-container" onClick={onEnter}>
        <img src="/images/logo/etchings2.png" alt="logo" className="logo"/>
      </div>
    );
  };
  
  export default Home;

