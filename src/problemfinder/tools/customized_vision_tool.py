from typing import Type
import os

from openai import AzureOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from crewai_tools.tools.base_tool import BaseTool

# Load environment variables from .env file
load_dotenv()

api_base = os.getenv("AZURE_API_BASE")
api_key= os.getenv("AZURE_API_KEY")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_version = os.getenv("AZURE_API_VERSION") # this might change in the future

client = AzureOpenAI(
    api_key=api_key,  
    api_version=api_version,
    base_url=f"{api_base}/openai/deployments/{deployment_name}"
)

class ImagePromptSchema(BaseModel):
    """Input for Vision Tool for Azure."""

    image_path_url: str = Field(..., description="The image path or URL.")


class CustomizedVisionTool(BaseTool):
    name: str = "Vision Tool for Azure"
    description: str = (
        "This tool uses Azure OpenAI's Vision API to extract the information from documents and images"
    )
    args_schema: Type[BaseModel] = ImagePromptSchema
   

    def _run_web_hosted_images(self, client, image_path_url: str) -> str:
        try:
            response = client.chat.completions.create(
                model=deployment_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": '''review the document carefully, 
                             extract all the information from it in a clear and concise way. 
                             ensure that all text in the image is returned in a way that will make it
                             easy to understand and use downstream'''},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_path_url},
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error processing web hosted image: {str(e)}"

    def _run(self, **kwargs) -> str:
        try:
            
            image_path_url = kwargs.get("image_path_url")

            if not image_path_url:
                return "Image Path or URL is required."

            return self._run_web_hosted_images(client, image_path_url)
   
        except Exception as e:
            return f"Error initializing Azure client: {str(e)}"

    