# GitHub guide for no-coder maintainers

## The simple picture

The **repository** is the shared folder for the project. A **branch** is a temporary copy used to make changes safely. A **pull request** is a review page that asks to move changes into `main`. When a pull request is merged, the changes become part of `main`; the temporary branch can usually be deleted. The **Actions** area runs automatic checks. The **default branch** is the branch shown first; for cpintl-org it is normally `main`.

## What the maintainer needs to know

You do not need to manage branches manually for routine work. Ask for a change in plain language. The adapter should inspect the repository, make a temporary branch when required, open a pull request, run checks, merge when authorized, delete the temporary branch, and confirm the final `main` URL. If a check fails, the change should stay out of `main` until the problem is fixed.

Keep only `main` when the repository is a small central hub and no release or recovery branch is required. Temporary branches may exist briefly during a change; they are not permanent project areas.

## Safe versus sensitive actions

Adding documentation, adding a validation workflow, opening a pull request, merging an already reviewed change, and deleting a merged temporary branch are ordinary repository maintenance. Deleting a repository, changing collaborators, changing authentication, changing billing, removing a protected branch, or publishing confidential content needs an explicit review of the exact target and effect.

## Recovery language

If something fails, use the terms **not completed**, **partly completed**, or **completed and verified**. Include the provider error, URL, commit, and next safe action. Never tell a maintainer that a change is complete based only on a local file.
