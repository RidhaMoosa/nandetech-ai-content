// 'use client';

import { useState } from 'react';
import { BarList, Card } from '@tremor/react';
import './index.css'
import './App.css'

const pages = [
  {
    name: 'Sumsang',
    value: 44,
  },
  {
    name: 'Apple',
    value: 20,
  },
  {
    name: 'Huawei',
    value: 17,
  },
  {
    name: 'Hisense',
    value: 3,
  },
  {
    name: 'OPPO',
    value: 3,
  },
  {
    name: 'Xiaom/Mi',
    value: 3,
  },
  {
    name: 'Honor',
    value: 2,
  },
  {
    name: 'Tecno',
    value: 2,
  },
  {
    name: 'Vivo',
    value: 2,
  },
  {
    name: 'Itel',
    value: 1,
  },
  {
    name: 'Mobicel',
    value: 1,
  },
  {
    name: 'Nokia',
    value: 1,
  },
  {
    name: 'Other',
    value: 2,
  },
];

const valueFormatter = (number: number | bigint) =>
  `${Intl.NumberFormat('us').format(number).toString()}%`;

export default function Product() {
  const [extended, setExtended] = useState(false);
  const [count, setCount] = useState(0);
  const handleBackClick = () => {
    window.history.back();
    window.location.reload();
    setCount(count + 1); // Force re-render by updating state
};
  return (
    <>
    
    <div style={{ textAlign: 'left'}}>
        <button onClick={handleBackClick} className="back-button">
        ← Back
        </button>
        </div>
   <div className='mt-6 mb-8 gap-4'>     
  <Card className="p-10 sm:mx-auto sm:max-w-2xl bg-gray-100"> 
  <h2>Most popular smart phone brands in South Africa as of September 2024</h2>        
    <div className="flex items-center justify-between border-b border-tremor-border p-6 dark:border-dark-tremor-border"> 
                
        <p className="\n font-medium text-tremor-content-strong dark:text-dark-tremor-content-strong">            
            <h3>Top brands</h3>          
            </p>          
            <p className="font-medium text-tremor-content-strong dark:text-dark-tremor-content-strong">            
                <h3>Sales</h3>          
                </p>        
                </div>       
                 <div          
                 className={` overflow-hidden p-6 ${extended ? '' : 'max-h-[260px]'}`}        
                 >          
                 <BarList data={pages} valueFormatter={valueFormatter} />        
                 </div>
    <div          
                className={`flex justify-center ${extended ? 
                'px-6 pb-6' : 'absolute inset-x-0 bottom-0 rounded-b-tremor-default bg-gradient-to-t from-tremor-background to-transparent py-7 dark:from-dark-tremor-background'          
                }`}        
                >          
                <button            
                className=" flex items-center justify-center rounded-tremor-small border border-tremor-border bg-tremor-background px-2.5 py-2 text-tremor-default font-medium text-tremor-content-strong shadow-tremor-input hover:bg-tremor-background-muted dark:border-dark-tremor-border dark:bg-dark-tremor-background dark:text-dark-tremor-content-strong dark:shadow-dark-tremor-input hover:dark:bg-dark-tremor-background-muted"            
                onClick={() => setExtended(!extended)}          
                >            
                {extended ? 'Show less' : 'Show more'}          
                </button>        
            </div>      
        </Card>
        </div>
        <div className="gap-6">
        <Card className="mx-auto mb-6 bg-yellow-100" decorationColor="indigo" >
        <div>
        <h2> Most popular smartphone brands in South Africa 2024
            Published by
            Umair Bashir
            ,
            Oct 22, 2024
            We asked South African consumers about "Most popular smartphone brands" and found that "Samsung" takes the top spot, while "Nokia" is at the other end of the ranking.
            These results are based on a representative online survey conducted in 2024 among 1,991 consumers in South Africa. </h2>
        </div>
        </Card>
        </div>
        
        
    </>

  );
}
