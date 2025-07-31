// src/WellnessPriorities.jsx

import React, { useState } from 'react';
import Header from './components/Header'; // 1. Import the reusable Header
import { DndContext, DragOverlay, PointerSensor, useSensor, useSensors, closestCorners, useDroppable } from '@dnd-kit/core';
import { arrayMove, SortableContext, useSortable, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { FaWeight, FaApple, FaShoePrints, FaMoon, FaDumbbell, FaHeartbeat, FaTint, FaSpa, FaBacon, FaHandPointer } from 'react-icons/fa';

// --- Reusable Item Component (for both lists) ---
const SortableItem = ({ id, content, icon, index, isTopGoal }) => {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({ id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0 : 1, // Hide the original item while dragging
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="flex items-center bg-white p-4 mb-3 rounded-lg shadow-sm"
    >
      {isTopGoal && (
        <span className="w-6 h-6 flex items-center justify-center bg-black text-white rounded-full mr-4 font-bold text-sm">{index + 1}</span>
      )}
      <span className="mr-3 text-gray-500">{icon}</span>
      <span className="flex-grow text-gray-800">{content}</span>
      <span className="text-gray-400">☰</span>
    </div>
  );
};

// --- Drag Overlay Item (non-sortable version for preview) ---
const DragItem = ({ content, icon }) => {
  return (
    <div className="flex items-center bg-white p-4 mb-3 rounded-lg shadow-sm opacity-100">
      <span className="mr-3 text-gray-500">{icon}</span>
      <span className="flex-grow text-gray-800">{content}</span>
      <span className="text-gray-400">☰</span>
    </div>
  );
};

// --- Main Page Component ---
const WellnessPriorities = () => {
  const initialGoals = {
    'available-goals': [
      { id: 'goal-1', content: 'Lose Weight', icon: <FaWeight /> },
      { id: 'goal-2', content: 'Improve Nutrition', icon: <FaBacon /> },
      { id: 'goal-3', content: 'Increase Daily Steps', icon: <FaShoePrints /> },
      { id: 'goal-4', content: 'Build Muscle', icon: <FaDumbbell /> },
      { id: 'goal-5', content: 'Improve Sleep Quality', icon: <FaMoon /> },
      { id: 'goal-6', content: 'Manage Stress', icon: <FaHeartbeat /> },
      { id: 'goal-7', content: 'Drink More Water', icon: <FaTint /> },
      { id: 'goal-8', content: 'Improve Flexibility', icon: <FaSpa /> },
    ],
    'top-goals': [],
  };

  const [items, setItems] = useState(initialGoals);
  const [activeId, setActiveId] = useState(null);
  const sensors = useSensors(useSensor(PointerSensor));

  const getItemById = (id) => {
    return items['available-goals'].find((goal) => goal.id === id) || items['top-goals'].find((goal) => goal.id === id);
  };

  // This is the core logic that now correctly handles moving items
  const handleDragEnd = ({ active, over }) => {
    setActiveId(null);
    if (!over) return;

    const activeContainer = active.data.current.sortable.containerId;
    const overContainer = over.data.current?.sortable.containerId || over.id;

    if (activeContainer !== overContainer) {
      // --- Handle moving items BETWEEN lists ---
      if (items['top-goals'].length >= 5 && overContainer === 'top-goals') {
        return; // Prevent adding more than 5 goals
      }
      
      const activeItems = items[activeContainer];
      const overItems = items[overContainer];
      
      const activeIndex = activeItems.findIndex(item => item.id === active.id);
      let overIndex = over.id in items ? overItems.length : overItems.findIndex(item => item.id === over.id);

      setItems(prev => ({
        ...prev,
        [activeContainer]: prev[activeContainer].filter(item => item.id !== active.id),
        [overContainer]: [
            ...prev[overContainer].slice(0, overIndex),
            activeItems[activeIndex],
            ...prev[overContainer].slice(overIndex, prev[overContainer].length)
        ]
      }));

    } else {
      // --- Handle reordering items WITHIN the same list ---
      const activeIndex = items[activeContainer].findIndex(item => item.id === active.id);
      const overIndex = items[overContainer].findIndex(item => item.id === over.id);

      if (activeIndex !== overIndex) {
        setItems(prev => ({
            ...prev,
            [overContainer]: arrayMove(prev[overContainer], activeIndex, overIndex)
        }));
      }
    }
  };

  const handleDragStart = ({ active }) => {
    setActiveId(active.id);
  };

  const handleDragCancel = () => {
    setActiveId(null);
  };

  return (
    // 2. Wrap the component's output in a React Fragment <>
    <>
      {/* 3. Add the Header component at the top */}
      <Header />

      <div className="bg-gray-50 min-h-screen flex flex-col items-center py-10 px-4">
        <div className="w-full max-w-4xl bg-white p-8 rounded-lg shadow-md">
          <h1 className="text-3xl font-bold text-center text-gray-800">Your Wellness Priorities</h1>
          <p className="text-center text-gray-500 mt-2 mb-8">
            Rank your top 5 wellness goals.
          </p>

          <DndContext 
            sensors={sensors} 
            collisionDetection={closestCorners} 
            onDragStart={handleDragStart}
            onDragEnd={handleDragEnd}
            onDragCancel={handleDragCancel}
          >
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              
              {/* --- Available Goals Column --- */}
              <AvailableGoalsContainer items={items['available-goals']} />

              {/* --- Your Top 5 Goals Column --- */}
              <TopGoalsContainer items={items['top-goals']} />
              
            </div>
            <DragOverlay>
              {activeId ? <DragItem {...getItemById(activeId)} /> : null}
            </DragOverlay>
          </DndContext>

          <div className="text-center mt-8">
            <button className="bg-black text-white font-bold py-3 px-8 rounded-lg hover:bg-gray-800 transition-colors">
              Done
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

// --- Available Goals Container ---
const AvailableGoalsContainer = ({ items }) => {
  const { setNodeRef } = useDroppable({ id: 'available-goals' });

  return (
    <div ref={setNodeRef} className="bg-gray-100 p-4 rounded-lg min-h-[400px]">
      <h2 className="text-xl font-semibold mb-4 text-gray-700">Available Goals</h2>
      <SortableContext id="available-goals" items={items.map(goal => goal.id)} strategy={verticalListSortingStrategy}>
        {items.map((goal, index) => (
          <SortableItem key={goal.id} id={goal.id} content={goal.content} icon={goal.icon} index={index} isTopGoal={false} />
        ))}
      </SortableContext>
    </div>
  );
};

// --- Top Goals Container ---
const TopGoalsContainer = ({ items }) => {
  const { setNodeRef } = useDroppable({ id: 'top-goals' });

  return (
    <div ref={setNodeRef} className="border-2 border-dashed rounded-lg p-4 min-h-[400px] border-gray-300">
      <h2 className="text-xl font-semibold mb-4 text-gray-700">Your Top 5 Goals</h2>
      <SortableContext id="top-goals" items={items.map(goal => goal.id)} strategy={verticalListSortingStrategy}>
        {items.length === 0 ? (
          <div className="flex flex-col items-center justify-start h-full text-gray-400 pt-5">
            <FaHandPointer className="text-4xl mb-2" />
            <p>Drag goals here to rank them</p>
          </div>
        ) : (
          items.map((goal, index) => (
            <SortableItem key={goal.id} id={goal.id} content={goal.content} icon={goal.icon} index={index} isTopGoal={true} />
          ))
        )}
      </SortableContext>
    </div>
  );
};

export default WellnessPriorities;