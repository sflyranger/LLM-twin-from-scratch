from loguru import logger 
from typing_extensions import Annotated
from zenml import get_step_context, step

from llm_engineering.application import utils
from llm_engineering.domain.documents import UserDocument

@step
def get_or_create_user(user_full_name: str) -> Annotated[UserDocument, "user"]:
    logger.info(f"Getting or creating user: {user_full_name}")

    # getting the first_name and last_name vars using the split_user_full_name function
    first_name, last_name = utils.split_user_full_name(user_full_name)

    # setting the user for the document based on the extracted first_name and last_name
    user = UserDocument.get_or_create(first_name=first_name, last_name=last_name)

    # setting the zenml step context
    step_context = get_step_context()
    # adding the user_full_name and user to the metadata
    step_context.add_output_metadata(output_name="user", metadata=_get_metadata(user_full_name, user))

    # returning the user
    return user

def _get_metadata(user_full_name: str, user: UserDocument)-> dict:
    """ Gets the user_full_name from the stored .yaml file and user from the UserDocument."""
    return {
        "query": {
            "user_full_name": user_full_name,
        },
        "retrieved": {
            "user_id": str(user.id), 
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    }

