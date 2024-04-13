import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ButtonToolbar from 'react-bootstrap/ButtonToolbar';

const Toolbar = ({setFeed}) => {
  return (
    <div className="top_bar">
    <div className="top_bar_left">
      <input type="text" className="view-textbox" value="View" readOnly />
    </div>
    <div className="top_bar_right">
      <ButtonGroup className="me-2 button-group" aria-label="First group">
        <Button onClick={()=>setFeed(0)}><span>1</span></Button> 
        <Button onClick={()=>setFeed(1)}><span>2</span></Button> 
        <Button onClick={()=>setFeed(2)}><span>3</span></Button>
        <Button onClick={()=>setFeed(3)}><span>4</span></Button>
        <Button onClick={()=>setFeed(4)}><span>5</span></Button>
      </ButtonGroup>
    </div>
  </div>
  );
}

export default Toolbar;
