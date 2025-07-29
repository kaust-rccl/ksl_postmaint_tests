22a23
> #include "proj_api.h"
237c238
<   if (status) cdoAbort("proj library error: %s", proj_errno_string(status));
---
>   if (status) cdoAbort("proj library error: %s", pj_strerrno(status));
289c290
<   if (status) cdoAbort("proj library error: %s", proj_errno_string(status));
---
>   if (status) cdoAbort("proj library error: %s", pj_strerrno(status));
380c381
<   if (status) cdoAbort("proj library error: %s", proj_errno_string(status));
---
>   if (status) cdoAbort("proj library error: %s", pj_strerrno(status));
430c431
<   if (status) cdoAbort("proj library error: %s", proj_errno_string(status));
---
>   if (status) cdoAbort("proj library error: %s", pj_strerrno(status));
510c511
<   if (status) cdoAbort("proj library error: %s", proj_errno_string(status));
---
>   if (status) cdoAbort("proj library error: %s", pj_strerrno(status));
605c606
<   if (status) cdoAbort("proj library error: %s", proj_errno_string(status));
---
>   if (status) cdoAbort("proj library error: %s", pj_strerrno(status));
618c619
<   if (status) cdoAbort("proj library error: %s", proj_errno_string(status));
---
>   if (status) cdoAbort("proj library error: %s", pj_strerrno(status));
