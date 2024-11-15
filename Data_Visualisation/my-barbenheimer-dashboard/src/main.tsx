import { StrictMode, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';
import Navigate from './navigate.tsx';
import Education from './education.tsx';
import Product from './product.tsx';

function RootComponent() {
  // State to track the active component, defaulting to 'Example'
  const [activeComponent, setActiveComponent] = useState('Example');
  
  // Conditionally render the selected component
  const renderComponent = () => {
    if (activeComponent === 'App') {
      return <App />;
    }else if (activeComponent === 'Product') {
      return <Product />;
    } else if (activeComponent === 'Example') {
      return <Navigate switchToApp={() => setActiveComponent('App')}
      switchToEdu={() => setActiveComponent('Education')} 
      switchToPro={() => setActiveComponent('Product')}
      />
      ;
    } else if (activeComponent == 'Education'){
      return <Education />;
    }
    return null;
  };

  return (
    <StrictMode>
      <main>{renderComponent()}</main>
    </StrictMode>
  );
}

// Render the RootComponent to the DOM
createRoot(document.getElementById('root')!).render(<RootComponent />);
