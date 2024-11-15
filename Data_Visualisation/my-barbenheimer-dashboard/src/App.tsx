import { useState } from 'react';
import { Card, Metric, Text, Title, DonutChart, LineChart } from "@tremor/react";
import './index.css'
import './App.css'

import dataBarbie from '../src/movie-barbie.json';
import dataOppenheimer from '../src/movie-oppenheimer.json';

const chartData = dataBarbie.domestic_daily.map(({ revenue, date }) => {
  const oppenheimer = dataOppenheimer.domestic_daily.find(opp => opp.date === date);
  return {
    date,
    Barbie: revenue,
    Oppenheimer: oppenheimer?.revenue
  }
})

function addCommasToNumber(number: number) {
  // Convert the number to a string
  let numString = number.toString();
  
  // Use regex to add commas to the string representation of the number
  numString = numString.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  
  return numString;
}

function App() {
  const [count, setCount] = useState(0);
  const handleBackClick = () => {
    window.history.back();
    window.location.reload();
    setCount(count + 1)
  }
  return (
    
    <div>
      <div style={{ textAlign: 'left'}}>
      <button onClick={handleBackClick} className="back-button" >
        ← Back
        </button>
      </div>
       <div>
       {dataBarbie.global_revenue > dataOppenheimer.global_revenue && (
            <Card className="max-w-xs mx-auto mb-6" decoration="top" decorationColor="indigo">
              <Text>Barbie's revenue exceeds Oppenheimer's by</Text>
              <Metric>${addCommasToNumber(dataBarbie.global_revenue - dataOppenheimer.global_revenue)}</Metric>
            </Card>
          )}
       </div>
      <div className="grid grid-cols-2 gap-12">
        <div>
          <h2 className="text-2xl font-bold mb-6">Barbie</h2>
          <div className="grid grid-cols-2 gap-12">
          <img src={dataBarbie.poster_path} alt="poster"/>
          <div>
            <div>
              <Title>User Rating</Title>
              <DonutChart
                className="text-2xl font-bold mt-6 mb-8 w-24 h-24"
                data={[
                  {
                    name: "total rating",
                    userScore: dataBarbie.vote_average,
                  },
                  {
                    name: false,
                    userScore: 10 - dataBarbie.vote_average,
                  }
                ]}
                category="userScore"
                index="name"
                colors={["green", "slate"]}
                label={`${(dataBarbie.vote_average * 10).toFixed()}%`}
              />
          </div>
          
          <Card className="max-w-xs mx-auto mb-6" decoration="top" decorationColor="indigo">
            <Text>Revenue</Text>
            <Metric>${ addCommasToNumber(dataBarbie.global_revenue) }</Metric>
          </Card>
          <Card className="max-w-xs mx-auto mb-6" decoration="top" decorationColor="indigo">
            <Text>Budget</Text>
            <Metric>${ addCommasToNumber(dataBarbie.budget) }</Metric>
          </Card>
        </div>
        </div>
        </div>
        <div>
          <h2 className="text-2xl font-bold mb-6">Oppenheimer</h2>
          <div className="grid grid-cols-2 gap-12">
          <img src={dataOppenheimer.poster_path} alt="poster"/>
          <div>
          <div>
              <Title>User Rating</Title>
              <DonutChart
                className="text-2xl font-bold mt-6 mb-8 w-24 h-24"
                data={[
                  {
                    name: "total rating",
                    userScore: dataOppenheimer.vote_average,
                  },
                  {
                    name: false,
                    userScore: 10 - dataOppenheimer.vote_average,
                  }
                ]}
                category="userScore"
                index="name"
                colors={["green", "slate"]}
                label={`${(dataOppenheimer.vote_average * 10).toFixed()}%`}
              />
            </div>
            <Card className="max-w-xs mx-auto mb-6" decoration="top" decorationColor="indigo">
              <Text>Revenue</Text>
              <Metric>${ addCommasToNumber(dataOppenheimer.global_revenue) }</Metric>
            </Card>
            
            <Card className="max-w-xs mx-auto mb-6" decoration="top" decorationColor="indigo">
              <Text>Budget</Text>
              <Metric>${ addCommasToNumber(dataOppenheimer.budget) }</Metric>
            </Card>
        </div>
      </div>
      </div>
      </div>
      <Card className="mt-8">
        <Title>Domestic Daily</Title>
        <LineChart
          className="mt-6"
          data={chartData}
          index="year"
          categories={["Barbie", "Oppenheimer"]}
          colors={["pink", "gray"]}
          yAxisWidth={120}
          valueFormatter={addCommasToNumber}
        />
      </Card>
    </div>
  )
}

export default App