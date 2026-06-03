module "eks_cluster" {
  source = "./modules/eks"

  cluster_name    = var.cluster_name
  vpc_id          = module.networking.vpc_id
  private_subnets = module.networking.private_subnets
}