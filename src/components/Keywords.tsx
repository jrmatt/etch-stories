import '../styles/Keywords.css';

interface KeywordProps {
    keyword: string;
    isActive: boolean;
    onClick: (keyword: string) => void;
}

function Keywords({ keyword, isActive, onClick }: KeywordProps ) {    
        return (
            <h4
                className={`Keyword ${isActive ? 'active' : ''}`}
                onClick={() => onClick(keyword)}
            >
                {keyword}
            </h4>
        );
}

export default Keywords;