import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np

def create_sensor_symbol(ax, x, y, size=1.0):
    """Create a generic sensor symbol"""
    # Circle for sensor
    circle = plt.Circle((x, y), size/2, fill=True, color='lightblue', edgecolor='blue', linewidth=2)
    ax.add_patch(circle)
    
    # Add "S" inside
    ax.text(x, y, "S", ha='center', va='center', fontsize=12, weight='bold')
    
    return x, y

def create_source_follower_symbol(ax, x, y, size=1.0):
    """Create a simplified source follower representation"""
    # Draw a simple box with "SF" inside
    rect = patches.Rectangle((x-size/2, y-size/2), size, size, 
                            linewidth=2, edgecolor='purple', facecolor='lavender')
    ax.add_patch(rect)
    
    # Add "SF" inside
    ax.text(x, y, "B", ha='center', va='center', fontsize=10, weight='bold')
    
    return x, y

def create_amplifier_symbol(ax, x, y, size=1.0):
    """Create a simplified amplifier symbol"""
    # Triangle for amplifier
    verts = [
        (x - size/2, y - size/2),  # left bottom
        (x + size/2, y),            # right middle
        (x - size/2, y + size/2)    # left top
    ]
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='lightyellow', edgecolor='k', linewidth=2)
    ax.add_patch(patch)
    
    # Add "+" sign inside
    ax.text(x, y, "+", ha='center', va='center', fontsize=14, weight='bold')
    
    return x, y

def create_output_symbol(ax, x, y, size=1.0):
    """Create a generic output symbol"""
    # Draw a simple arrow pointing right
    ax.arrow(x-size/2, y, size, 0, head_width=size/2, 
            head_length=size/3, fc='green', ec='green', linewidth=2)
    
    # Add "Out" label
    ax.text(x+size/2, y, "Out", ha='left', va='center', fontsize=10, weight='bold', color='green')
    
    return x, y

def main():
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # First sensor path (e.g., humidity)
    sensor1_x, sensor1_y = create_sensor_symbol(ax, 2, 4)
    sf1_x, sf1_y = create_source_follower_symbol(ax, 4, 4)
    amp1_x, amp1_y = create_amplifier_symbol(ax, 6, 4)
    out1_x, out1_y = create_output_symbol(ax, 8, 4)

    
    # Connect components with arrows
    # First path connections
    ax.arrow(sensor1_x + 0.5, sensor1_y, 1.0, 0, head_width=0.1, 
            head_length=0.2, fc='k', ec='k', linewidth=1.5)
    ax.arrow(sf1_x + 0.5, sf1_y, 1.0, 0, head_width=0.1, 
            head_length=0.2, fc='k', ec='k', linewidth=1.5)
    ax.arrow(amp1_x + 0.5, amp1_y, 1.0, 0, head_width=0.1, 
            head_length=0.2, fc='k', ec='k', linewidth=1.5)

    # Add labels
    ax.text(2, 4.7, "Sensor", ha='center', va='center', fontsize=12)
    ax.text(4, 4.7, "Buffer", ha='center', va='center', fontsize=12)
    ax.text(6, 4.7, "Amplifier", ha='center', va='center', fontsize=12)
    ax.text(8, 4.7, "Output", ha='center', va='center', fontsize=12)
    
    # Add path labels
    #ax.text(0.5, 4, "Humidity Path", ha='left', va='center', fontsize=12, 
    #        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    #ax.text(0.5, 2, "Temperature Path", ha='left', va='center', fontsize=12,
    #        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
    
    # Set axis limits and remove ticks
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')
    ax.axis('off')


    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()