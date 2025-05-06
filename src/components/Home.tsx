import "../styles/Home.css"

interface HomeProps {
    onEnter: () => void;
  }
  
  const Home: React.FC<HomeProps> = ({ onEnter }) => {
    return (
      <div className="home-container" onClick={onEnter}>
        <img src="/images/logo/etchings2.png" alt="logo" className="logo"/>
        <div>
          <h1 className="site-intro">written impressions from real conversations</h1>
        </div>
      </div>
    );
  };
  
  export default Home;

