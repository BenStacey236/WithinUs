import pygame

class Barrier:
    def __init__(self, points: list[tuple[int]]) -> None:
        self.points = points


    def is_collided(self, targetPoint) -> bool:
        """
        Check if the targetPoint is inside the polygon defined by self.points.
        
        :param tuple[int] targetPoint: Tuple of integers (x, y).
        :return isCollided: Boolean, True if targetPoint is inside the polygon, False otherwise.
        """
        
        x, y = targetPoint
        y = -y
        n = len(self.points)
        isCollided = False

        px, py = self.points[0]
        for i in range(n + 1):
            sx, sy = self.points[i % n]

            # Checks to see if y-coordinate is in bounds
            if y <= min(py, sy) or y > max(py, sy):
                px, py = sx, sy
                continue
                
            # Checks to see if x-coordinate is in bounds
            if x > max(px, sx):
                px, py = sx, sy
                continue
            
            # Avoiding division by zero
            if py != sy:
                xIntersect = (y - py) * (sx - px) / (sy - py) + px
            # Handle horizontal lines explicitly
            else: 
                xIntersect = px

            if x <= xIntersect:
                isCollided = not isCollided

            # Move to next edge
            px, py = sx, sy

        return isCollided
    

    def __repr__(self) -> str:
        '''Returns a string representation of the barrier object'''

        reprStr = "Barrier with verticies: "
        for point in self.points:
            reprStr += str(point)

        return reprStr