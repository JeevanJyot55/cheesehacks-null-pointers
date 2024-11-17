'use client';

import React, { useState } from 'react';
import { Button } from "./button";
import { Input } from "./input";
import { Slider } from "./slider";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./card";

interface Stock {
  name: string;
  sector: string;
  quantity: number;
}

export default function OptiStock() {
  const [showStartScreen, setShowStartScreen] = useState(true);
  const [budget, setBudget] = useState<number>(0);
  const [risk, setSliderValue] = useState<number[]>([50]);
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:5000/allocate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ budget, risk: risk[0] }),
      });
      const data = await response.json();
      const formattedStocks = data.map((item: any) => ({
        name: item.Symbol,
        sector: item.Sector,
        quantity: item.Quantity,
      }));
      setStocks(formattedStocks);
    } catch (error) {
      console.error('Error fetching stock recommendations:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (showStartScreen) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-black to-gray-900 text-white flex flex-col items-center justify-center px-6">
        <h1 className="text-7xl font-extrabold mb-8">OptiStock</h1>
        <p className="text-2xl mb-12 text-center">Smart stock recommendations tailored for you.</p>
        <Button
          onClick={() => setShowStartScreen(false)}
          className="bg-blue-600 text-white hover:bg-blue-700 text-lg py-4 px-12 rounded-lg shadow-lg transition duration-300"
        >
          Get Started
        </Button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-6">
      <Card className="w-full max-w-5xl bg-gray-800 shadow-2xl rounded-3xl overflow-hidden">
        <CardHeader className="bg-blue-600 text-white py-8 px-12">
          <CardTitle className="text-4xl font-bold">OptiStock</CardTitle>
          <CardDescription className="text-gray-200 text-xl mt-2">
            Enter your budget and risk tolerance to get started.
          </CardDescription>
        </CardHeader>
        <CardContent className="py-12 px-16">
          <form onSubmit={handleSubmit} className="space-y-8">
            <div>
              <label htmlFor="budget" className="block text-lg font-medium text-gray-200 mb-2">
                Budget ($)
              </label>
              <Input
                type="number"
                id="budget"
                value={budget === 0 ? '' : budget}
                onChange={(e) => setBudget(e.target.value === '' ? 0 : Number(e.target.value))}
                min="0"
                step="1"
                required
                className="w-full h-14 rounded-lg bg-gray-700 text-white placeholder-gray-400 border-gray-600 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
            </div>
            <div>
              <label htmlFor="risk" className="block text-lg font-medium text-gray-200 mb-2">
                Risk Factor: {risk[0]}
              </label>
              <Slider
                id="risk"
                min={0}
                max={100}
                step={1}
                value={risk}
                onValueChange={setSliderValue}
                className={`w-full ${risk[0] > 75 ? 'animate-[shake_0.5s_ease-in-out]' : ''}`}
              />
              <div className="flex justify-between text-sm text-gray-400 mt-2">
                <span>Very Safe</span>
                <span>Very Risky</span>
              </div>
            </div>
            <Button
              type="submit"
              disabled={isLoading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white text-lg font-semibold py-4 rounded-lg transition duration-150 ease-in-out"
            >
              {isLoading ? 'Processing...' : 'Get Recommendations'}
            </Button>
          </form>
        </CardContent>
      </Card>

      {stocks.length > 0 && (
        <Card className="w-full max-w-5xl mt-8 bg-gray-800 shadow-2xl rounded-3xl overflow-hidden">
          <CardHeader className="bg-blue-600 text-white py-6 px-12">
            <CardTitle className="text-3xl font-semibold">Recommended Stocks</CardTitle>
          </CardHeader>
          <CardContent className="py-8 px-12">
            <ul className="divide-y divide-gray-700">
              {stocks.map((stock, index) => (
                <li key={index} className="py-6 flex justify-between items-center">
                  <div className="flex flex-col">
                    <span className="text-lg font-medium text-white">{stock.name}</span>
                    <span className="text-sm text-gray-400">{stock.sector}</span>
                  </div>
                  <span className="text-lg font-medium text-white">{stock.quantity} shares</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
