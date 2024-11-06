import joblib

def save_model_with_description(model, description, filename):
    """
    Save a model with a description using joblib.

    Parameters:
    - model: The trained model to save (e.g., a scikit-learn estimator).
    - description: A string describing the model (e.g., "RandomForest model trained on dataset X").
    - filename: The name of the file to save the model and description to, with .joblib extension.

    Returns:
    None
    """
    # Create a dictionary containing both the model and the description
    data_to_save = {
        'model': model,
        'description': description
    }
    
    # Save the dictionary to a joblib file
    joblib.dump(data_to_save, filename)
    print(f"Model and description saved to {filename}")

def load_model_with_description(filename):
    loaded_data = joblib.load("filename")
    model = loaded_data['model']
    description = loaded_data['description']
    return model, description