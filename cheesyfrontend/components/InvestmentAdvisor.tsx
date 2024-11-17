'use client'

import React, { useState } from 'react';
import { Button } from "./button"
import { Input } from "./input"
import { Slider } from "./slider"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./card"

interface Stock {
  name: string;
  quantity: number;
}

export default function InvestmentAdvisor() {
  const [budget, setBudget] = useState<number>(0);
  const [risk, setSliderValue] = useState<number[]>([50]);
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const getSliderClass = () => {
    return risk[0] > 50 ? "shaking high-risk" : "";
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch('http://your-api-endpoint.com/getStocks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ budget, sliderValue: risk }),
      });
      const data = await response.json();
      setStocks(data);
    } catch (error) {
      console.error('Error fetching stocks:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Investment Advisor</CardTitle>
          <CardDescription>Enter your budget and risk tolerance to get stock recommendations</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="budget" className="block text-sm font-medium text-gray-700">Budget ($)</label>
              <input
                type="number"
                id="budget"
                value={budget === 0 ? '' : budget} // Set to empty string if the value is zero
                onChange={(e) => {
                  const value = e.target.value;
                  setBudget(value === '' ? 0 : Number(value)); // Handle empty string
                }}
                min="0"
                step="1"
                required
              />
            </div>
            <div className="mb-6">
              <label
                htmlFor="risk"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Risk Factor: {risk[0]}
              </label>
              <div className="space-y-2">
                <Slider
                  id="risk"
                  min={0}
                  max={100}
                  step={1}
                  value={risk}
                  onValueChange={setSliderValue}
                  className={getSliderClass()}
                />
                <div className="flex justify-between text-sm text-gray-500">
                  <span>Very Safe / Low Reward</span>
                  <span>Very Risky / High Reward</span>
                </div>
              </div>
            </div>

            <Button type="submit" disabled={isLoading}>
              {isLoading ? 'Loading...' : 'Get Recommendations'}
            </Button>
          </form>
        </CardContent>
      </Card>

      {stocks.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Recommended Stocks</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {stocks.map((stock, index) => (
                <li key={index} className="flex justify-between items-center border-b py-2">
                  <span className="font-medium">{stock.name}</span>
                  <span>{stock.quantity} shares</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  );
}