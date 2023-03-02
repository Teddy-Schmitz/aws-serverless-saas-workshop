import { MatSnackBar } from '@angular/material/snack-bar';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent implements OnInit {
  submitting: boolean = false;
  tenantForm: FormGroup = this.fb.group({
    tenantName: ['', [Validators.required]],
    tenantEmail: ['', [Validators.email, Validators.required]],
    tenantTier: ['', [Validators.required]],
    tenantPhone: [''],
    tenantAddress: [''],
  });

  subscriptionID = '';
  stripeID = '';

  constructor(
    private fb: FormBuilder,
    private _snackBar: MatSnackBar,
    private http: HttpClient,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.tenantForm.disable();
    this.route.queryParams.subscribe((params: { [x: string]: string; }) => {
      this.subscriptionID = params['id'];
      this.http.get(`${environment.apiGatewayUrl}/subscription/${this.subscriptionID}`).subscribe((sub: any) => {
        const subscription = sub.message;
        console.log(subscription);
        this.tenantForm.enable();
        // Add subscription data line below this


        
        this.tenantForm.controls['tenantEmail'].disable();
        this.tenantForm.controls['tenantTier'].disable();
        this.stripeID = subscription.customer;
      });
    });
  }

  openErrorMessageSnackBar(errorMessage: string) {
    this._snackBar.open(errorMessage, 'Dismiss', {
      duration: 4 * 1000, // seconds
    });
  }

  submit() {
    this.submitting = true;
    this.tenantForm.disable();
    const tenant = {
      stripeID: this.stripeID,
      ...this.tenantForm.value,
    };
    this.http
      .post(`${environment.apiGatewayUrl}/registration`, tenant)
      .subscribe({
        next: () => {
          this.openErrorMessageSnackBar('Successfully created new tenant!');
          this.tenantForm.reset();
          this.tenantForm.enable();
          this.submitting = false;
        },
        error: (err: any) => {
          this.openErrorMessageSnackBar('An unexpected error occurred!');
          console.error(err);
          this.tenantForm.enable();
          this.submitting = false;
        },
      });
  }
}
