
import { useState } from 'react';
import { BarChart, Card, Divider, Switch } from '@tremor/react';
import { DonutChart } from "@tremor/react";
import './index.css'
import './App.css'
import education from './educational-tertiary.json'


const data = [

    {    date: 'Jan 23',    
        'This Year': 68560,    
        'Last Year': 28560,  
    },  
    {    date: 'Feb 23',    
        'This Year': 70320,    
        'Last Year': 30320,  
    },  
    {    date: 'Mar 23',    
        'This Year': 80233,    
        'Last Year': 70233,  
    },  
    {    date: 'Apr 23',    
        'This Year': 55123,    
        'Last Year': 45123,  
    },  
    {    date: 'May 23',    
        'This Year': 56000,    
        'Last Year': 80600,  
    },  
    {    date: 'Jun 23',    
        'This Year': 100000,    
        'Last Year': 85390,  
    },  
    {    date: 'Jul 23',    
        'This Year': 85390,    
        'Last Year': 45340,  
    },  
    {    date: 'Aug 23',    
        'This Year': 80100,    
        'Last Year': 70120,  
    },  
    {    date: 'Sep 23',    
        'This Year': 75090,    
        'Last Year': 69450,  
    },  
    {    date: 'Oct 23',    
        'This Year': 71080,    
        'Last Year': 63345,  
    },  
    {    date: 'Nov 23',    
        'This Year': 61210,    
        'Last Year': 100330,  
    },  
    {    date: 'Dec 23',    
        'This Year': 60143,    
        'Last Year': 45321,  
    },
];


const barData = [
    {
        "headline": 5.7,
        'tertiary': 8.9,
        date:'Jan 2013'
    },
    {
        "headline": 6.1,
        "tertiary": 9.3,
         date: 2014 
     },
     {
        "headline": 4.6,
        "tertiary": 9.9,
         date: 2015
     },
     {
        "headline": 6.3,
        "tertiary": 0,
         date: 2016
     },
     {
        "headline": 5.3,
        "tertiary": 6.3,
         date: 2017
     },
     {
        "headline": 4.6,
        "tertiary": 5.2,
         date: 2018
     },
     {
        "headline": 6.2,
        "tertiary": 4.1,
         date: 2019
     },
     {
        "headline": 3.3,
        "tertiary": 4.7,
         date: 2020
     },
     {
        "headline": 4.6,
        "tertiary": 5.2,
         date: 2021
     }
];


export default function Education(){ 
    const [showComparison, setShowComparison] = useState(false);
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
        <div className='mt-6 mb-8 gap-6'>
        <Card className="sm:mx-auto sm:max-w-2xl">        
            <h3 className="ml-1 mr-1 font-semibold text-tremor-content-strong dark:text-dark-tremor-content-strong">          
            Annual percentage change in tertiary education fees and headline CPI.        
                </h3>        
                <p className="text-tremor-default text-tremor-content dark:text-dark-tremor-content">          
                            
                    </p>  
                    <h2 className="chart-title">Tertiary Education Fees</h2>       
                    <BarChart          
                    data={barData}          
                    index="date"          
                    categories={           
                        showComparison ? ['headline', 'tertiary'] : ['tertiary']          
                    }  
                    valueFormatter={(number: number) =>          
                        `${Intl.NumberFormat("us").format(number).toString()}%`        
                    }           
                    colors={showComparison ? ['cyan', 'blue'] : ['blue']}          
                        
                    yAxisWidth={50}          
                    className="mt-6 hidden h-60 sm:block"        
                    /> 
                         
                    <BarChart
                              
                    data={barData}          
                    index="headline"          
                    categories={            
                        showComparison ? ['headline', 'tertiary'] : ['tertiary']          
                    }          
                    colors={showComparison ? ['cyan', 'blue'] : ['blue']}          
                           
                    showYAxis={false}          
                    className="mt-4 h-56 sm:hidden"        
                    />        
                    <Divider />        
                    <div className="mb-2 flex items-center space-x-3">          
                        <Switch            
                        id="comparison"            
                        onChange={() => setShowComparison(!showComparison)}          
                        />          
                        <label            
                        htmlFor="comparison"            
                        className="text-tremor-default text-tremor-content dark:text-dark-tremor-content"          
                        >            
                        Show both tertiary and headline          
                        </label> 
                              
                    </div> 
                    <h3>source: Stats SA</h3>      
                </Card> 
                </div>
                <Card>
                    <div className="flex flex-col gap-12">    
                    <div className="flex flex-col items-center justify-center gap-4">      
                    <p className="text-gray-700 dark:text-gray-300">Total Income</p>      
                    <DonutChart        
                    // data={total_income}
                    data={[
                    {
                      name: "government grants",
                      userScore: education.Government_grants,
                    },
                    {
                        name: "other",
                        userScore: education.other,
                    },
                    {
                        name: "turtion_fees",
                        userScore: education.Turtion_fees,
                    },
                    ]
                    }       
                    variant="pie"        
                    category="userScore" 
                                   
                    valueFormatter={(number: number) =>          
                        `${Intl.NumberFormat("us").format(number).toString()}%`        
                    }      
                    />    
                    </div>  
                    </div>
                    </Card>
                </>
                  
            );
        }

     
    
    