resource "local_file" "pet" {
    content  = "This is a pet file"
    filename = "${path.module}/pet.txt"
}