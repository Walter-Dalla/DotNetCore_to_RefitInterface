# DotNetCore_to_RefitInterface
This code snippet is an refit interface generator, it looks in your .net core project for endpoints and translates in to a refit interface


# How to use
python .\refit.py {your entire file path}

## Example:
python .\refit.py F:\Projects\ProjectName


# !!Important!!
The [Route] annotation need to be on the line above the class definition

## Example:
[ApiController]
[Route("api/[controller]")]
public class StartRoutingController : ControllerBase