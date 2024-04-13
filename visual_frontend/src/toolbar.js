import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ButtonToolbar from 'react-bootstrap/ButtonToolbar';

function ToolbarBasicExample() {
  return (
    <div className="top_bar">
    <div className="top_bar_left">
      <input type="text" className="view-textbox" value="View" readOnly />
    </div>
    <div className="top_bar_right">
      <ButtonGroup className="me-2 button-group" aria-label="First group">
        <Button><span>1</span></Button> 
        <Button><span>2</span></Button> 
        <Button><span>3</span></Button>
        <Button><span>4</span></Button>
        <Button><span>5</span></Button>
      </ButtonGroup>
    </div>
  </div>
  );
}



export default ToolbarBasicExample;