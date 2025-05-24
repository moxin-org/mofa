"""
Main entry point for the integrated workflow.
"""
import asyncio
import logging
import sys

# Import components
from src.config import parse_arguments, setup_logging, load_kling_config, load_beatoven_config
from src.keyframe_processor import KeyframeProcessor
from src.workflow import IntegratedWorkflow

async def main():
    """Main function to run the workflow."""
    # Parse command-line arguments
    args = parse_arguments()
    
    # Setup logging
    setup_logging(logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        # Load KlingDemo configuration
        try:
            kling_config = load_kling_config(args.env_file)
            logger.info("Loaded KlingDemo configuration successfully")
        except Exception as e:
            logger.error(f"Failed to load KlingDemo configuration: {e}")
            sys.exit(1)
        
        # Load Beatoven configuration if needed
        beatoven_config = load_beatoven_config(args.beatoven_env_file)
        beatoven_api_key = beatoven_config.get('api_key')
        beatoven_api_url = beatoven_config.get('api_url')
        
        # Create output directory
        args.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Parse keyframes
        keyframe_processor = KeyframeProcessor()
        try:
            keyframes_data = keyframe_processor.parse_keyframes(args.keyframes_file)
            logger.info(f"Parsed {len(keyframes_data)} keyframes from {args.keyframes_file}")
        except Exception as e:
            logger.error(f"Failed to parse keyframes file: {e}")
            sys.exit(1)
        
        # Initialize and run workflow
        workflow = IntegratedWorkflow(
            kling_config=kling_config,
            output_dir=args.output_dir,
            use_dify=args.use_dify,
            beatoven_api_key=beatoven_api_key,
            beatoven_api_url=beatoven_api_url,
            music_prompt=args.music_prompt,
            music_filename=args.music_filename
        )
        
        # Process keyframes
        results = await workflow.process_keyframes(keyframes_data, args.model_name)
        
        # Print summary of results
        print("\n=== Workflow Results ===")
        for frame_id, assets in results.items():
            print(f"\nKeyframe: {frame_id}")
            print(f"  Image: {assets['image']}")
            print(f"  Video: {assets['video']}")
            if 'music' in assets:
                print(f"  Music: {assets['music']}")
            else:
                print("  Music: None")
        
        print("\nWorkflow completed successfully!")
        
    except Exception as e:
        logger.error(f"Error running workflow: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())