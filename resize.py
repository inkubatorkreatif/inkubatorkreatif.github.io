#resize with maximum size using PIL
from PIL import Image
import sys
import argparse
import logging
import time
import traceback
import numpy as np
import os

def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def resize_image(image_path, output_path, max_size, logger):
    """
    Resize image while maintaining aspect ratio so that the largest dimension
    does not exceed max_size
    
    Args:
        image_path (str): Path to the source image
        output_path (str): Path for the resized image
        max_size (int): Maximum width or height in pixels
        logger (logging.Logger): Logger instance
    
    Returns:
        tuple: New dimensions (width, height)
    """
    try:
        # Open the image
        logger.info(f"Opening image: {image_path}")
        img = Image.open(image_path)
        
        # Get original dimensions
        width, height = img.size
        logger.info(f"Original dimensions: {width}x{height}")
        
        # Calculate new dimensions while maintaining aspect ratio
        if width > height:
            # Width is the largest dimension
            if width <= max_size:
                logger.info(f"Image already smaller than max_size ({max_size}px)")
                if output_path != image_path:
                    img.save(output_path)
                return width, height
            
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            # Height is the largest dimension
            if height <= max_size:
                logger.info(f"Image already smaller than max_size ({max_size}px)")
                if output_path != image_path:
                    img.save(output_path)
                return width, height
                
            new_height = max_size
            new_width = int(width * (max_size / height))
        
        # Resize the image
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Save the resized image
        resized_img.save(output_path)
        logger.info(f"Resized image saved to: {output_path}")
        logger.info(f"New dimensions: {new_width}x{new_height}")
        
        return new_width, new_height
        
    except Exception as e:
        logger.error(f"Error resizing image: {str(e)}")
        logger.error(traceback.format_exc())
        raise

def main():
    """Main function to handle command-line usage"""
    parser = argparse.ArgumentParser(description="Resize images while maintaining aspect ratio")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("-o", "--output", help="Output image path (defaults to overwriting input)")
    parser.add_argument("-s", "--max-size", type=int, default=1024,
                        help="Maximum size of the largest dimension in pixels (default: 1024)")
    parser.add_argument("-b", "--batch", action="store_true",
                        help="Process a directory of images instead of a single file")
    
    args = parser.parse_args()
    logger = setup_logging()
    
    try:
        if args.batch:
            if not os.path.isdir(args.input):
                logger.error(f"{args.input} is not a directory")
                return 1
                
            output_dir = args.output if args.output else args.input
            os.makedirs(output_dir, exist_ok=True)
            
            count = 0
            start_time = time.time()
            
            for filename in os.listdir(args.input):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                    input_path = os.path.join(args.input, filename)
                    output_path = os.path.join(output_dir, filename)
                    
                    try:
                        resize_image(input_path, output_path, args.max_size, logger)
                        count += 1
                    except Exception as e:
                        logger.error(f"Failed to process {filename}: {str(e)}")
            
            elapsed = time.time() - start_time
            logger.info(f"Batch processing completed: {count} images in {elapsed:.2f} seconds")
        
        else:
            # Process a single image
            if not os.path.isfile(args.input):
                logger.error(f"{args.input} is not a file")
                return 1
                
            output_path = args.output if args.output else args.input
            
            start_time = time.time()
            resize_image(args.input, output_path, args.max_size, logger)
            elapsed = time.time() - start_time
            logger.info(f"Processing completed in {elapsed:.2f} seconds")
        
        return 0
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())