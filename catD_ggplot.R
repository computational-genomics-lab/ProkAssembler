# Install patchwork if not already installed
if (!requireNamespace("patchwork", quietly = TRUE)) {
  install.packages("patchwork")
}

# Load necessary libraries
library(ggplot2)
library(dplyr)
library(tidyr)
library(viridis)
library(patchwork)

# Updated dataset
data <- data.frame(
  Organism = rep(c("Sphaerospermopsis torques-reginae ITEP", "Thermostichus lividus PCC 6715", "Scytonema millei VB511283", "Tolypothrix campylonemoides VB511288", "simulated category D"), each = 4),
  AssemblyProcess = rep(paste("Assembly", 1:4), times = 5),
  CheckM_completeness = c(93.33, 90.78, 99.33, 98.11, 74.76, 86.6, 99.53, 74, 99.76, 99.76, 99.76, 88.48, 99.76, 99.76, 97.11, 99.63, 99.37, 99.97, 99.97, 99.97),
  Contamination = c(31.48, 30.02, 0, 0, 30, 30, 0.12, 0, 1.19, 1.19, 1.04, 2.34, 1.19, 1.19, 0.8, 1.89, 3.96, 6.35, 0.04, 0.04),
  Heterogeneity = c(93.88, 92.78, 0, 0, 82.78, 62.7,0, 0, 33.33, 33.33, 2.01, 16.67, 33.33, 33.33, 0, 0, 91.67, 97.62, 0, 0) ,
  No_of_Contigs = c(100, 100, 15, 89, 100, 100, 28, 200,8, 8, 36, 641, 7, 8, 30, 71, 47, 65, 19, 27),
  Genome_size = c(7.1, 6.9, 5.1, 5, 8.3, 8.8, 2.6, 2.6, 10, 10, 10, 6, 9.9, 10, 9.4, 6.6, 5.9, 6.7, 5.3, 5.2),
  Busco_completeness = c(88.1, 88.7, 99.4,98.4, 42.90, 53.6, 96.6, 42, 99.6, 99.6, 99.4, 79.6, 99.6, 99.6, 97.8, 98.7, 99.8, 100, 100, 100)
)
# Map AssemblyProcess to new labels
data$AssemblyProcess <- factor(data$AssemblyProcess,
                                levels = paste("Assembly", 1:4),
                                labels = c("Nocon assembly", "Lowcon assembly", "Highcon assembly", "HighconHetero assembly"))

# Set the levels for the Organism factor to maintain the original order
data$Organism <- factor(data$Organism, levels = unique(data$Organism))

# Function to create a plot for each organism
create_plot <- function(organism) {
  # Filter data for the current organism
  filtered_data <- data %>% filter(Organism == organism)

  # Reshape data for ggplot
  plot_data <- filtered_data %>%
    pivot_longer(cols = c(CheckM_completeness, Contamination, Heterogeneity, No_of_Contigs, Genome_size, Busco_completeness),
                 names_to = "Parameter", values_to = "Value")

  # Plot using ggplot
  p <- ggplot(plot_data, aes(x = Parameter, y = AssemblyProcess, color = Value, size = Value)) +
    geom_point() +
    scale_color_gradient(low = "blue", high = "red") +
    theme_minimal() +
    labs(title = paste(organism),
         x = NULL, # Remove x-axis label
         y = NULL, # Remove y-axis label
         color = "Value",
         size = "Value") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          plot.title = element_text(size = 10),  # Adjust the title font size here
         legend.position = "none")  # Remove the legend
  return(p)
}

# List of organisms
organisms <- unique(data$Organism)

# Create a list of plots
plots <- lapply(organisms, create_plot)
# Combine plots using patchwork in a grid layout
combined_plot <- wrap_plots(plots) +
  plot_layout(ncol = 5, byrow = TRUE)  # Arrange in 1 row

# Save the combined plot as a single PDF
ggsave(filename = "D.pdf", plot = combined_plot, width = 23, height = 4)

