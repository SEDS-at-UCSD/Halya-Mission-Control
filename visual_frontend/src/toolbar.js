import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ButtonToolbar from 'react-bootstrap/ButtonToolbar';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTableCellsLarge } from '@fortawesome/free-solid-svg-icons';





const Toolbar = ({setFeed, values}) => {
  return (
    <div className="top_bar">
    <div className="top_bar_right">
      <ButtonGroup className="me-2 button-group" aria-label="First group">
        <Button onClick={()=>setFeed(0)} className={values.includes(0) ? "shown" : ""}><span>1</span></Button> 
        <Button onClick={()=>setFeed(1)} className={values.includes(1) ? "shown" : ""}><span>2</span></Button> 
        <Button onClick={()=>setFeed(2)} className={values.includes(2) ? "shown" : ""}><span>3</span></Button>
        <Button onClick={()=>setFeed(3)} className={values.includes(3) ? "shown" : ""}><span>4</span></Button>
        <Button onClick={()=>setFeed(4)} className={values.includes(4) ? "shown last_btn" : "last_btn"}><span>5</span></Button>
      </ButtonGroup>
    </div>

    <div className="view_switch">
    <ButtonGroup className="me-2 button-group" aria-label="First group">
        <Button> <FontAwesomeIcon icon={faTableCellsLarge} /> </Button> 
        <Button><img></img></Button> 
        
      </ButtonGroup>
    </div>

    

  </div>
  );
}

export default Toolbar;
