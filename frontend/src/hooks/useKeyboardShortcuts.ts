import { useEffect, useCallback, useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { addNode } from '../store/flowSlice';
import { createNode } from '../utils/nodeFactory';
import { Node } from 'reactflow'; // Import Node type from reactflow
import { AppDispatch } from '../store/store'; // Import AppDispatch type

interface Position {
  x: number;
  y: number;
}

interface CustomNode extends Node {
  type: string;
  position: Position;
  data: {
    title?: string;
    acronym?: string;
    color?: string;
    config?: any; // You might want to define a more specific type
    input?: any;  // You might want to define a more specific type
    output?: any; // You might want to define a more specific type
    [key: string]: any;
  };
}

export const useKeyboardShortcuts = (
  selectedNodeID: string | null,
  nodes: CustomNode[],
  dispatch: AppDispatch
) => {
  const [copiedNode, setCopiedNode] = useState<CustomNode | null>(null);

  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      if (event.metaKey || event.ctrlKey) {
        switch (event.key) {
          case 'c': // CMD + C or CTRL + C
            if (selectedNodeID) {
              const nodeToCopy = nodes.find((node) => node.id === selectedNodeID);
              if (nodeToCopy) {
                setCopiedNode(nodeToCopy);
              }
            }
            break;
          case 'v': // CMD + V or CTRL + V
            if (copiedNode) {
              const newNode = createNode(
                copiedNode.type,
                uuidv4(),
                {
                  x: copiedNode.position.x + 50,
                  y: copiedNode.position.y + 50,
                },
                copiedNode.data
              );
              dispatch(addNode({ node: newNode }));
            }
            break;
          default:
            break;
        }
      }
    },
    [selectedNodeID, copiedNode, nodes, dispatch]
  );

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleKeyDown]);

  return { copiedNode, setCopiedNode };
};